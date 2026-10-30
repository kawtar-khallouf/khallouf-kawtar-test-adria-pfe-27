package com.adria.transactionservice.web.rest;
import com.adria.transactionservice.service.TransactionService;
import com.adria.transactionservice.service.TransactionDtos.*;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.HttpStatus;
@RestController @RequestMapping("/api/transfers") public class TransferRestController {
 private final TransactionService service;public TransferRestController(TransactionService service){this.service=service;}
 @PostMapping @ResponseStatus(HttpStatus.CREATED) public TransferResult transfer(@Valid @RequestBody CreateTransfer req){return service.transfer(req);}
}
