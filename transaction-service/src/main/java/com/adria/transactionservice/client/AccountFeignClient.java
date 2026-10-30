package com.adria.transactionservice.client;
import com.adria.transactionservice.service.TransactionDtos.*;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.*;
import java.util.UUID;
@FeignClient(name="account-service")
public interface AccountFeignClient {
 @GetMapping("/api/accounts/{id}") RemoteAccount get(@PathVariable("id") UUID id);
 @PostMapping("/internal/accounts/{id}/debit") RemoteAccount debit(@PathVariable("id") UUID id,@RequestBody Money money);
 @PostMapping("/internal/accounts/{id}/credit") RemoteAccount credit(@PathVariable("id") UUID id,@RequestBody Money money);
 @PostMapping("/internal/accounts/transfer") void transfer(@RequestBody InternalTransfer transfer);
}
