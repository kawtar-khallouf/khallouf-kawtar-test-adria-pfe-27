package com.adria.transactionservice.service;
import com.adria.transactionservice.service.TransactionDtos.*;
import java.util.*;
public interface TransactionService {
 TransactionView create(CreateTransaction request);
 TransferResult transfer(CreateTransfer request);
 List<TransactionView> list();
 TransactionView get(UUID id);
 List<TransactionView> byAccount(UUID id);
}
