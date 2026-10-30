package com.adria.accountservice.mcp;
import com.adria.accountservice.service.*;
import com.adria.accountservice.service.AccountDtos.*;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.context.annotation.*;
import org.springframework.stereotype.Component;
import java.util.*;
@Component public class AccountTools {
 private final AccountService service;public AccountTools(AccountService service){this.service=service;}
 @Tool(description="List bank accounts with available balances and statuses") public List<AccountView> listBankAccounts(){return service.list();}
 @Tool(description="Get bank account by its UUID") public AccountView findBankAccount(String id){return service.find(UUID.fromString(id));}
 @Configuration public static class ToolsConfig {
  @Bean ToolCallbackProvider accountToolProvider(AccountTools tools){return MethodToolCallbackProvider.builder().toolObjects(tools).build();}
 }
}
