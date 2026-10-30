package com.adria.transactionservice.mcp;
import com.adria.transactionservice.service.*;
import com.adria.transactionservice.service.TransactionDtos.*;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.context.annotation.*;
import org.springframework.stereotype.Component;
import java.util.*;import java.math.BigDecimal;
@Component public class TransactionTools {
 private final TransactionService service;public TransactionTools(TransactionService service){this.service=service;}
 @Tool(description="List transactions in the bank") public List<TransactionView> listBankTransactions(){return service.list();}
 @Tool(description="Find transactions of one account UUID") public List<TransactionView> findAccountTransactions(String accountId){return service.byAccount(UUID.fromString(accountId));}
 @Tool(description="Register a positive bank transaction; verify the account, currency and configured limit")
 public TransactionView registerBankTransaction(String accountId,String amount,String currency,String merchantCategory,String country){
  return service.create(new CreateTransaction(UUID.fromString(accountId),new BigDecimal(amount),currency,merchantCategory,country));
 }
 @Tool(description="Transfer money between two bank accounts in the same currency")
 public TransferResult executeBankTransfer(String fromAccountId,String toAccountId,String amount,String currency){
  return service.transfer(new CreateTransfer(UUID.fromString(fromAccountId),UUID.fromString(toAccountId),new BigDecimal(amount),currency));
 }
 @Configuration public static class ToolsConfig {
  @Bean ToolCallbackProvider transactionToolProvider(TransactionTools tools){return MethodToolCallbackProvider.builder().toolObjects(tools).build();}
 }
}
