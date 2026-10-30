package com.adria.transactionservice.repository;
import com.adria.transactionservice.domain.OutboxEvent;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.*;
public interface OutboxRepository extends JpaRepository<OutboxEvent,UUID>{List<OutboxEvent> findTop50ByPublishedAtIsNullOrderByCreatedAtAsc();}
