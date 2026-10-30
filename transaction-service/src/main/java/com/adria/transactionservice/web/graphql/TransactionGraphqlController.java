package com.adria.transactionservice.web.graphql;
import com.adria.transactionservice.service.*;
import com.adria.transactionservice.service.TransactionDtos.*;
import org.springframework.graphql.data.method.annotation.*;
import org.springframework.stereotype.Controller;
import java.util.*;import java.math.BigDecimal;
@Controller public class TransactionGraphqlController {
 private final TransactionService service;public TransactionGraphqlController(TransactionService service){this.service=service;}
 @QueryMapping public List<TransactionView> transactions(){return service.list();}
 @QueryMapping public TransactionView transaction(@Argument String id){return service.get(UUID.fromString(id));}
 @MutationMapping public TransactionView registerTransaction(@Argument String accountId,@Argument String amount,@Argument String currency,@Argument String merchantCategory,@Argument String country){return service.create(new CreateTransaction(UUID.fromString(accountId),new BigDecimal(amount),currency,merchantCategory,country));}
}
