package com.adria.accountservice.web.rest;
import com.adria.accountservice.service.*;
import com.adria.accountservice.service.AccountDtos.*;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.HttpStatus;
import java.util.*;
@RestController @RequestMapping("/api/accounts")
public class AccountRestController {
 private final AccountService service;public AccountRestController(AccountService service){this.service=service;}
 @GetMapping public List<AccountView> all(){return service.list();}
 @GetMapping("/{id}") public AccountView get(@PathVariable UUID id){return service.find(id);}
 @PostMapping @ResponseStatus(HttpStatus.CREATED) public AccountView create(@Valid @RequestBody CreateAccount input){return service.create(input);}
 @PatchMapping("/{id}/status") public AccountView status(@PathVariable UUID id,@Valid @RequestBody StatusUpdate input){return service.status(id,input);}
}
