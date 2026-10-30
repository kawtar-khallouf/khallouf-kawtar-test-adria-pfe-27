package com.adria.accountservice.service;
import com.adria.accountservice.domain.*;
import com.adria.accountservice.repository.*;
import com.adria.accountservice.service.AccountDtos.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
import java.math.BigDecimal;
import java.util.*;
@Service @Transactional
public class AccountServiceImpl implements AccountService {
 private final AccountRepository accounts; private final BalanceOperationRepository operations;
 public AccountServiceImpl(AccountRepository accounts,BalanceOperationRepository operations){this.accounts=accounts;this.operations=operations;}
 private AccountView view(Account a){return new AccountView(a.getId(),a.getCustomerReference(),a.getStatus(),a.getCurrency(),a.getBalance());}
 private Account locked(UUID id){return accounts.locked(id).orElseThrow(()->new ResponseStatusException(HttpStatus.NOT_FOUND,"Account not found: "+id));}
 private void validate(Account a,BigDecimal amount,String currency){
  if(a.getStatus()!=AccountStatus.ACTIVE)throw new ResponseStatusException(HttpStatus.CONFLICT,"Account blocked");
  if(!a.getCurrency().equalsIgnoreCase(currency))throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Currency mismatch");
  if(amount==null || amount.signum()<=0)throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Amount must be positive");
 }
 @Override public AccountView create(CreateAccount request){
  if(!Double.isFinite(request.balance())||request.balance()<0) throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Invalid opening balance");
  Account a=new Account(UUID.randomUUID(),request.customerReference(),AccountStatus.ACTIVE,request.currency().toUpperCase(Locale.ROOT),request.balance());
  return view(accounts.save(a));
 }
 @Override @Transactional(readOnly=true) public AccountView find(UUID id){return accounts.findById(id).map(this::view).orElseThrow(()->new ResponseStatusException(HttpStatus.NOT_FOUND,"Account not found"));}
 @Override @Transactional(readOnly=true) public List<AccountView> list(){return accounts.findAll().stream().map(this::view).toList();}
 @Override public AccountView status(UUID id,StatusUpdate status){Account a=locked(id);a.setStatus(status.status());return view(a);}
 @Override public AccountView debit(UUID id,Money req){
  Account a=locked(id);
  if(operations.existsByOperationId(req.operationId()))return view(a);
  validate(a,req.amount(),req.currency());
  BigDecimal newBalance=BigDecimal.valueOf(a.getBalance()).subtract(req.amount());
  if(newBalance.signum()<0)throw new ResponseStatusException(HttpStatus.CONFLICT,"Insufficient funds");
  a.setBalance(newBalance.doubleValue());operations.saveAndFlush(new BalanceOperation(req.operationId(),"DEBIT"));return view(a);
 }
 @Override public AccountView credit(UUID id,Money req){
  Account a=locked(id);
  if(operations.existsByOperationId(req.operationId()))return view(a);
  validate(a,req.amount(),req.currency());
  a.setBalance(BigDecimal.valueOf(a.getBalance()).add(req.amount()).doubleValue());
  operations.saveAndFlush(new BalanceOperation(req.operationId(),"CREDIT"));return view(a);
 }
 @Override public void transfer(Transfer req){
  if(req.sourceId().equals(req.destinationId()))throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Accounts must be different");
  UUID first=req.sourceId().compareTo(req.destinationId())<0?req.sourceId():req.destinationId();
  UUID second=req.sourceId().equals(first)?req.destinationId():req.sourceId();
  Account a=locked(first);Account b=locked(second);
  if(operations.existsByOperationId(req.operationId()))return;
  Account source=a.getId().equals(req.sourceId())?a:b;Account dest=a.getId().equals(req.destinationId())?a:b;
  validate(source,req.amount(),req.currency());validate(dest,req.amount(),req.currency());
  BigDecimal remaining=BigDecimal.valueOf(source.getBalance()).subtract(req.amount());
  if(remaining.signum()<0)throw new ResponseStatusException(HttpStatus.CONFLICT,"Insufficient funds");
  source.setBalance(remaining.doubleValue());dest.setBalance(BigDecimal.valueOf(dest.getBalance()).add(req.amount()).doubleValue());
  operations.saveAndFlush(new BalanceOperation(req.operationId(),"TRANSFER"));
 }
}
