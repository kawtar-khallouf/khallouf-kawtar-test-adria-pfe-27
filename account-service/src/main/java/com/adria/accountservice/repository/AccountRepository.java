package com.adria.accountservice.repository;
import com.adria.accountservice.domain.Account;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import jakarta.persistence.LockModeType;
import org.springframework.data.repository.query.Param;
import java.util.*;
public interface AccountRepository extends JpaRepository<Account,UUID> {
 @Lock(LockModeType.PESSIMISTIC_WRITE) @Query("select a from Account a where a.id=:id") Optional<Account> locked(@Param("id") UUID id);
}
