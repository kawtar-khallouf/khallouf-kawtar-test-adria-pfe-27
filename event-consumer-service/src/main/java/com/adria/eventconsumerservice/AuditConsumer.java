package com.adria.eventconsumerservice;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.slf4j.*;
import org.springframework.stereotype.Component;
@Component public class AuditConsumer {
 private static final Logger log=LoggerFactory.getLogger(AuditConsumer.class);
 @KafkaListener(topics="bank.transactions.created",groupId="bank-audit-group")
 public void onCreated(String payload,@Header(KafkaHeaders.RECEIVED_KEY) String accountId){
  log.info("AUDIT TransactionCreated, accountId={}, event={}",accountId,payload);
  // Intentionally read-only: no bank data is mutated.
 }
}
