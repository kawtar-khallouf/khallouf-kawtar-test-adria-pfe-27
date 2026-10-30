package com.adria.accountservice.config;
import com.adria.accountservice.service.AccountService;
import com.adria.accountservice.service.AccountDtos.CreateAccount;
import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.*;
@Configuration public class AccountDemoData {
 @Bean @Profile("demo") ApplicationRunner demoAccounts(AccountService service){return args->{service.create(new CreateAccount("CUST-001","EUR",4000));service.create(new CreateAccount("CUST-002","EUR",1500));};}
}
