package com.adria.transactionservice.repository;
import com.adria.transactionservice.domain.BankTransaction;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.*;
public interface TransactionRepository extends JpaRepository<BankTransaction,UUID>{List<BankTransaction> findByAccountId(UUID accountId);}
