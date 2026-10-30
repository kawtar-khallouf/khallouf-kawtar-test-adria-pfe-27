package com.adria.transactionservice.service;
import com.adria.transactionservice.client.AccountRemoteService;
import com.adria.transactionservice.domain.BankTransaction;
import com.adria.transactionservice.repository.TransactionRepository;
import com.adria.transactionservice.service.TransactionDtos.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import java.math.*;import java.util.*;import java.time.Instant;
@Service public class TransactionServiceImpl implements TransactionService {
 private final TransactionRepository transactions;private final TransactionStore store;private final AccountRemoteService accounts;private final BigDecimal maxAmount;
 public TransactionServiceImpl(TransactionRepository transactions,TransactionStore store,AccountRemoteService accounts,@Value("${bank.transaction.max-amount:1000}") BigDecimal maxAmount){this.transactions=transactions;this.store=store;this.accounts=accounts;this.maxAmount=maxAmount;}
 private TransactionView view(BankTransaction t){return new TransactionView(t.getId(),t.getAccountId(),t.getAmount(),t.getCurrency(),t.getMerchantCategory(),t.getCountry(),t.getCreatedAt(),t.getTransactionType(),t.getTransferReference());}
 private void amount(BigDecimal a){if(a==null||a.signum()<=0)throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Amount must be positive");if(a.compareTo(maxAmount)>0)throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Max amount: "+maxAmount);if(a.scale()>2)throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Only 2 decimal places allowed");}
 private void check(RemoteAccount a,String currency){if(!"ACTIVE".equals(a.status()))throw new ResponseStatusException(HttpStatus.CONFLICT,"Account blocked");if(!a.currency().equalsIgnoreCase(currency))throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Currency mismatch");}
 @Override public TransactionView create(CreateTransaction r){
  amount(r.amount()); RemoteAccount a=accounts.get(r.accountId());check(a,r.currency());
  UUID id=UUID.randomUUID();
  accounts.debit(r.accountId(),new Money(r.amount(),r.currency(),id));
  BankTransaction t=new BankTransaction(id,r.accountId(),r.amount(),r.currency().toUpperCase(Locale.ROOT),r.merchantCategory(),r.country(),Instant.now(),"PURCHASE",null);
  try{store.persist(List.of(t));}catch(RuntimeException e){
   try{accounts.credit(r.accountId(),new Money(r.amount(),r.currency(),UUID.nameUUIDFromBytes((id+"-refund").getBytes(java.nio.charset.StandardCharsets.UTF_8))));}
   catch(RuntimeException compensationError){e.addSuppressed(compensationError);}
   throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR,"Persistence failed; check compensation log",e);
  }
  return view(t);
 }
 @Override public TransferResult transfer(CreateTransfer r){
  amount(r.amount());if(r.sourceId().equals(r.destinationId()))throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Accounts must be different");
  check(accounts.get(r.sourceId()),r.currency());check(accounts.get(r.destinationId()),r.currency());
  UUID transferId=UUID.randomUUID(), debitId=UUID.randomUUID(),creditId=UUID.randomUUID();
  accounts.transfer(new InternalTransfer(r.sourceId(),r.destinationId(),r.amount(),r.currency(),transferId));
  Instant now=Instant.now();
  BankTransaction debit=new BankTransaction(debitId,r.sourceId(),r.amount(),r.currency().toUpperCase(Locale.ROOT),"TRANSFER","N/A",now,"TRANSFER_OUT",transferId);
  BankTransaction credit=new BankTransaction(creditId,r.destinationId(),r.amount(),r.currency().toUpperCase(Locale.ROOT),"TRANSFER","N/A",now,"TRANSFER_IN",transferId);
  try{store.persist(List.of(debit,credit));}catch(RuntimeException e){
   try{accounts.transfer(new InternalTransfer(r.destinationId(),r.sourceId(),r.amount(),r.currency(),UUID.nameUUIDFromBytes((transferId+"-reverse").getBytes(java.nio.charset.StandardCharsets.UTF_8))));}
   catch(RuntimeException compensationError){e.addSuppressed(compensationError);}
   throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR,"Transfer recording failed; check compensation",e);
  }
  return new TransferResult(transferId,view(debit),view(credit));
 }
 @Override public List<TransactionView> list(){return transactions.findAll().stream().map(this::view).toList();}
 @Override public TransactionView get(UUID id){return transactions.findById(id).map(this::view).orElseThrow(()->new ResponseStatusException(HttpStatus.NOT_FOUND,"Transaction not found"));}
 @Override public List<TransactionView> byAccount(UUID id){return transactions.findByAccountId(id).stream().map(this::view).toList();}
}
