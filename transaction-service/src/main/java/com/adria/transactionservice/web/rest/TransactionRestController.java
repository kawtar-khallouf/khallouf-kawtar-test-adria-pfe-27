package com.adria.transactionservice.web.rest;
import com.adria.transactionservice.service.TransactionService;
import com.adria.transactionservice.service.TransactionDtos.*;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import java.util.*;
@RestController @RequestMapping("/api/transactions") public class TransactionRestController {
 private final TransactionService service;public TransactionRestController(TransactionService service){this.service=service;}
 @GetMapping public List<TransactionView> all(@RequestParam(required=false) UUID accountId){return accountId==null?service.list():service.byAccount(accountId);}
 @GetMapping("/{id}") public TransactionView get(@PathVariable UUID id){return service.get(id);}
 @PostMapping @ResponseStatus(HttpStatus.CREATED) public TransactionView create(@Valid @RequestBody CreateTransaction req){return service.create(req);}
}
