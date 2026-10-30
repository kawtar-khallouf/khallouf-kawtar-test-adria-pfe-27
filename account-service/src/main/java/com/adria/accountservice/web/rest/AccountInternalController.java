package com.adria.accountservice.web.rest;
import com.adria.accountservice.service.AccountService;
import com.adria.accountservice.service.AccountDtos.*;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;
import java.util.UUID;
@RestController @RequestMapping("/internal/accounts")
public class AccountInternalController {
 private final AccountService service;public AccountInternalController(AccountService service){this.service=service;}
 @PostMapping("/{id}/debit") public AccountView debit(@PathVariable UUID id,@Valid @RequestBody Money money){return service.debit(id,money);}
 @PostMapping("/{id}/credit") public AccountView credit(@PathVariable UUID id,@Valid @RequestBody Money money){return service.credit(id,money);}
 @PostMapping("/transfer") public void transfer(@Valid @RequestBody Transfer req){service.transfer(req);}
}
