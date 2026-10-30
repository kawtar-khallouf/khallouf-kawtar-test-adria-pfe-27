package com.adria.transactionservice;
import com.adria.transactionservice.client.AccountRemoteService;
import com.adria.transactionservice.repository.TransactionRepository;
import com.adria.transactionservice.service.*;
import com.adria.transactionservice.service.TransactionDtos.*;
import org.junit.jupiter.api.Test;
import org.springframework.web.server.ResponseStatusException;
import java.math.BigDecimal;import java.util.*;
import static org.junit.jupiter.api.Assertions.*;import static org.mockito.Mockito.*;
class TransactionServiceImplTest {
 private final TransactionRepository repo=mock(TransactionRepository.class);
 private final TransactionStore store=mock(TransactionStore.class);
 private final AccountRemoteService accounts=mock(AccountRemoteService.class);
 private final TransactionService service=new TransactionServiceImpl(repo,store,accounts,new BigDecimal("1000"));
 @Test void amountOverConfiguredLimitIsRejectedBeforeFeign(){
  CreateTransaction req=new CreateTransaction(UUID.randomUUID(),new BigDecimal("1000.01"),"EUR","SHOP","MA");
  assertThrows(ResponseStatusException.class,()->service.create(req));verifyNoInteractions(accounts,store);
 }
 @Test void accountCurrencyMismatchIsRejected(){
  UUID id=UUID.randomUUID();when(accounts.get(id)).thenReturn(new RemoteAccount(id,"C1","ACTIVE","EUR",100));
  assertThrows(ResponseStatusException.class,()->service.create(new CreateTransaction(id,new BigDecimal("20"),"USD","SHOP","MA")));
  verify(accounts,never()).debit(any(),any());
 }
 @Test void validTransactionDebitsAndPersists(){
  UUID id=UUID.randomUUID();when(accounts.get(id)).thenReturn(new RemoteAccount(id,"C1","ACTIVE","EUR",100));
  TransactionView result=service.create(new CreateTransaction(id,new BigDecimal("20"),"EUR","SHOP","MA"));
  assertEquals(id,result.accountId());verify(accounts).debit(eq(id),any(Money.class));verify(store).persist(anyList());
 }
}
