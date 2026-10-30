package com.adria.accountservice.domain;
import jakarta.persistence.*;
import java.util.UUID;
@Entity @Table(name="balance_operations",uniqueConstraints=@UniqueConstraint(columnNames="operation_id"))
public class BalanceOperation {
 @Id @GeneratedValue(strategy=GenerationType.UUID) private UUID id;
 @Column(name="operation_id",nullable=false,unique=true) private UUID operationId;
 @Column(nullable=false) private String operationType;
 protected BalanceOperation(){} public BalanceOperation(UUID op,String type){operationId=op;operationType=type;}
}
