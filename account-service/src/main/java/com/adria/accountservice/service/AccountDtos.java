package com.adria.accountservice.service;
import com.adria.accountservice.domain.AccountStatus;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;
import java.util.UUID;
public final class AccountDtos {
 private AccountDtos(){}
 public record CreateAccount(@NotBlank String customerReference, @NotBlank String currency, @DecimalMin("0.0") double balance){}
 public record AccountView(UUID id,String customerReference,AccountStatus status,String currency,double balance){}
 public record Money(@NotNull @DecimalMin(value="0.0",inclusive=false) BigDecimal amount,@NotBlank String currency,@NotNull UUID operationId){}
 public record Transfer(@NotNull UUID sourceId,@NotNull UUID destinationId,@NotNull @DecimalMin(value="0.0",inclusive=false) BigDecimal amount,@NotBlank String currency,@NotNull UUID operationId){}
 public record StatusUpdate(@NotNull AccountStatus status){}
}
