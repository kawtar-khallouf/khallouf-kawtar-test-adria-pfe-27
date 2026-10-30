package com.adria.transactionservice.service;
import com.adria.transactionservice.repository.OutboxRepository;
import com.adria.transactionservice.domain.OutboxEvent;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import org.slf4j.*;
import java.util.concurrent.TimeUnit;
@Component @EnableScheduling public class OutboxPublisher {
 private static final Logger log=LoggerFactory.getLogger(OutboxPublisher.class);
 private final OutboxRepository outbox;private final KafkaTemplate<String,String> kafka;private final String topic;
 public OutboxPublisher(OutboxRepository outbox,KafkaTemplate<String,String> kafka,@Value("${bank.events.topic:bank.transactions.created}") String topic){this.outbox=outbox;this.kafka=kafka;this.topic=topic;}
 @Scheduled(fixedDelayString="${bank.events.poll-delay-ms:3000}")
 @Transactional public void flush(){
  for(OutboxEvent e:outbox.findTop50ByPublishedAtIsNullOrderByCreatedAtAsc()){
   try{kafka.send(topic,e.getAggregateId().toString(),e.getPayload()).get(5,TimeUnit.SECONDS);e.markPublished();}
   catch(Exception error){log.warn("Kafka publishing failed for {} - will retry",e.getId(),error);break;}
  }
 }
}
