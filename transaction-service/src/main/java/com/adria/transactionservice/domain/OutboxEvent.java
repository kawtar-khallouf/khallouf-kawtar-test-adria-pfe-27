package com.adria.transactionservice.domain;
import jakarta.persistence.*;import java.util.UUID;import java.time.Instant;
@Entity @Table(name="transaction_outbox")
public class OutboxEvent {
 @Id private UUID id;
 @Column(nullable=false) private UUID aggregateId;
 @Lob @Column(nullable=false) private String payload;
 @Column(nullable=false) private Instant createdAt;
 private Instant publishedAt;
 protected OutboxEvent(){}
 public OutboxEvent(UUID id,UUID aggregateId,String payload){this.id=id;this.aggregateId=aggregateId;this.payload=payload;this.createdAt=Instant.now();}
 public UUID getId(){return id;}public UUID getAggregateId(){return aggregateId;}public String getPayload(){return payload;}
 public Instant getCreatedAt(){return createdAt;}public Instant getPublishedAt(){return publishedAt;}
 public void markPublished(){publishedAt=Instant.now();}
}
