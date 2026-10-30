package com.adria.transactionservice.domain;
import jakarta.persistence.*;
import java.util.*;import java.math.BigDecimal;import java.time.Instant;
@Entity @Table(name="bank_transactions")
public class BankTransaction {
 @Id private UUID id;
 @Column(nullable=false) private UUID accountId;
 @Column(nullable=false,precision=19,scale=2) private BigDecimal amount;
 @Column(nullable=false) private String currency;
 private String merchantCategory;
 private String country;
 @Column(nullable=false) private Instant createdAt;
 @Column(nullable=false) private String transactionType;
 private UUID transferReference;
 protected BankTransaction(){}
 public BankTransaction(UUID id,UUID accountId,BigDecimal amount,String currency,String merchantCategory,String country,Instant at,String type,UUID transferRef){
  this.id=id;this.accountId=accountId;this.amount=amount;this.currency=currency;this.merchantCategory=merchantCategory;this.country=country;this.createdAt=at;this.transactionType=type;this.transferReference=transferRef;
 }
 public UUID getId(){return id;}public UUID getAccountId(){return accountId;}public BigDecimal getAmount(){return amount;}public String getCurrency(){return currency;}
 public String getMerchantCategory(){return merchantCategory;}public String getCountry(){return country;}
 public Instant getCreatedAt(){return createdAt;}public String getTransactionType(){return transactionType;}public UUID getTransferReference(){return transferReference;}
}
