package com.adria.transactionservice.service;
import com.adria.transactionservice.domain.*;
import com.adria.transactionservice.repository.*;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.*;
@Service public class TransactionStore {
 private final TransactionRepository transactions;private final OutboxRepository outbox;private final ObjectMapper mapper;
 public TransactionStore(TransactionRepository transactions,OutboxRepository outbox,ObjectMapper mapper){this.transactions=transactions;this.outbox=outbox;this.mapper=mapper;}
 @Transactional public void persist(List<BankTransaction> items){
  for(BankTransaction item:items){
   transactions.save(item);
   try{
    Map<String,Object> event=new LinkedHashMap<>();event.put("eventId",UUID.randomUUID());event.put("eventType","TransactionCreated");
    event.put("transactionId",item.getId());event.put("accountId",item.getAccountId());event.put("amount",item.getAmount());
    event.put("currency",item.getCurrency());event.put("occurredAt",item.getCreatedAt());
    outbox.save(new OutboxEvent(UUID.randomUUID(),item.getAccountId(),mapper.writeValueAsString(event)));
   }catch(JsonProcessingException ex){throw new IllegalStateException("Cannot serialize event",ex);}
  }
 }
}
