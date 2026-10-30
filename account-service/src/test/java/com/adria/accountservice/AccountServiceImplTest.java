package com.adria.accountservice;
import com.adria.accountservice.domain.*;
import com.adria.accountservice.repository.*;
import com.adria.accountservice.service.*;
import com.adria.accountservice.service.AccountDtos.*;
import org.junit.jupiter.api.*;
import org.mockito.*;
import org.springframework.web.server.ResponseStatusException;
import java.util.*;import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;import static org.mockito.Mockito.*;
class AccountServiceImplTest {
 private final AccountRepository accounts=mock(AccountRepository.class);
 private final BalanceOperationRepository operations=mock(BalanceOperationRepository.class);
 private final AccountService service=new AccountServiceImpl(accounts,operations);
 @Test void debitUpdatesBalanceOnce() {
  UUID id=UUID.randomUUID(),op=UUID.randomUUID();Account a=new Account(id,"C-1",AccountStatus.ACTIVE,"EUR",200);
  when(accounts.locked(id)).thenReturn(Optional.of(a));
  when(operations.existsByOperationId(op)).thenReturn(false,true);
  assertEquals(150.0,service.debit(id,new Money(new BigDecimal("50"),"EUR",op)).balance(),0.0001);
  assertEquals(150.0,service.debit(id,new Money(new BigDecimal("50"),"EUR",op)).balance(),0.0001);
  verify(operations,times(1)).saveAndFlush(any(BalanceOperation.class));
 }
 @Test void insufficientFundsDoNotDebit(){
  UUID id=UUID.randomUUID();when(accounts.locked(id)).thenReturn(Optional.of(new Account(id,"C-1",AccountStatus.ACTIVE,"EUR",10)));
  assertThrows(ResponseStatusException.class,()->service.debit(id,new Money(new BigDecimal("50"),"EUR",UUID.randomUUID())));
  verify(operations,never()).saveAndFlush(any());
 }
 @Test void blockedAccountDoesNotDebit(){
  UUID id=UUID.randomUUID();when(accounts.locked(id)).thenReturn(Optional.of(new Account(id,"C-1",AccountStatus.BLOCKED,"EUR",100)));
  assertThrows(ResponseStatusException.class,()->service.debit(id,new Money(new BigDecimal("3"),"EUR",UUID.randomUUID())));
 }
 @Test void wrongCurrencyRejected(){
  UUID id=UUID.randomUUID();when(accounts.locked(id)).thenReturn(Optional.of(new Account(id,"C-1",AccountStatus.ACTIVE,"EUR",100)));
  assertThrows(ResponseStatusException.class,()->service.debit(id,new Money(new BigDecimal("3"),"USD",UUID.randomUUID())));
 }
}
