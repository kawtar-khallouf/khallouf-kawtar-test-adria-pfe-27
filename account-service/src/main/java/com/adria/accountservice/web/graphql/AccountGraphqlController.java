package com.adria.accountservice.web.graphql;
import com.adria.accountservice.service.*;
import com.adria.accountservice.service.AccountDtos.*;
import org.springframework.graphql.data.method.annotation.*;
import org.springframework.stereotype.Controller;
import java.util.*;
@Controller public class AccountGraphqlController {
 private final AccountService accounts;public AccountGraphqlController(AccountService accounts){this.accounts=accounts;}
 @QueryMapping public List<AccountView> accounts(){return accounts.list();}
 @QueryMapping public AccountView account(@Argument String id){return accounts.find(UUID.fromString(id));}
 @MutationMapping public AccountView openAccount(@Argument String customerReference,@Argument String currency,@Argument double balance){return accounts.create(new CreateAccount(customerReference,currency,balance));}
}
