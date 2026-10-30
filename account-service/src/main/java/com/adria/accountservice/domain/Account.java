package com.adria.accountservice.domain;
import jakarta.persistence.*;
import java.util.UUID;
@Entity @Table(name="bank_accounts")
public class Account {
 @Id private UUID id;
 @Column(nullable=false) private String customerReference;
 @Enumerated(EnumType.STRING) @Column(nullable=false) private AccountStatus status;
 @Column(nullable=false) private String currency;
 @Column(nullable=false) private double balance;
 protected Account() {}
 public Account(UUID id,String ref,AccountStatus status,String currency,double balance){this.id=id;this.customerReference=ref;this.status=status;this.currency=currency;this.balance=balance;}
 public UUID getId(){return id;} public String getCustomerReference(){return customerReference;}
 public AccountStatus getStatus(){return status;}public String getCurrency(){return currency;}public double getBalance(){return balance;}
 public void setStatus(AccountStatus v){status=v;}public void setBalance(double v){balance=v;}
}
