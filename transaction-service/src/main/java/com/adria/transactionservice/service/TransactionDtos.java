package com.adria.transactionservice.service;
import jakarta.validation.constraints.*;
import java.util.*;import java.time.Instant;import java.math.BigDecimal;
public final class TransactionDtos {
 private TransactionDtos(){}
 public record CreateTransaction(@NotNull UUID accountId,@NotNull @DecimalMin(value="0.0",inclusive=false) BigDecimal amount,@NotBlank String currency,@NotBlank String merchantCategory,@NotBlank String country){}
 public record CreateTransfer(@NotNull UUID sourceId,@NotNull UUID destinationId,@NotNull @DecimalMin(value="0.0",inclusive=false) BigDecimal amount,@NotBlank String currency){}
 public record TransactionView(UUID id,UUID accountId,BigDecimal amount,String currency,String merchantCategory,String country,Instant createdAt,String transactionType,UUID transferReference){}
 public record TransferResult(UUID transferId,TransactionView debit,TransactionView credit){}
 public record RemoteAccount(UUID id,String customerReference,String status,String currency,double balance){}
 public record Money(BigDecimal amount,String currency,UUID operationId){}
 public record InternalTransfer(UUID sourceId,UUID destinationId,BigDecimal amount,String currency,UUID operationId){}
}
