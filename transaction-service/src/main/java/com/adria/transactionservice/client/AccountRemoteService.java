package com.adria.transactionservice.client;
import com.adria.transactionservice.service.TransactionDtos.*;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
import java.util.UUID;
import feign.FeignException;
@Service public class AccountRemoteService {
 private final AccountFeignClient feign;public AccountRemoteService(AccountFeignClient feign){this.feign=feign;}
 @CircuitBreaker(name="account-service",fallbackMethod="accountFallback")
 public RemoteAccount get(UUID id){return feign.get(id);}
 public RemoteAccount accountFallback(UUID id,Throwable error){propagateClientError(error);throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,"Account service unavailable",error);}
 @CircuitBreaker(name="account-service",fallbackMethod="moneyFallback")
 public RemoteAccount debit(UUID id,Money m){return feign.debit(id,m);}
 @CircuitBreaker(name="account-service",fallbackMethod="moneyFallback")
 public RemoteAccount credit(UUID id,Money m){return feign.credit(id,m);}
 public RemoteAccount moneyFallback(UUID id,Money m,Throwable error){propagateClientError(error);throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,"Account balance change unavailable",error);}
 @CircuitBreaker(name="account-service",fallbackMethod="transferFallback")
 public void transfer(InternalTransfer t){feign.transfer(t);}
 public void transferFallback(InternalTransfer t,Throwable error){propagateClientError(error);throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,"Transfer unavailable",error);}
 private void propagateClientError(Throwable error){
  if(error instanceof FeignException e && e.status()>=400 && e.status()<500)
    throw new ResponseStatusException(HttpStatus.valueOf(e.status()),e.contentUTF8(),e);
 }
}
