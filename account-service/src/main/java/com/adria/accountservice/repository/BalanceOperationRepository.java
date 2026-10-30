package com.adria.accountservice.repository;
import com.adria.accountservice.domain.BalanceOperation;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;
public interface BalanceOperationRepository extends JpaRepository<BalanceOperation,UUID> {
 boolean existsByOperationId(UUID operationId);
}
