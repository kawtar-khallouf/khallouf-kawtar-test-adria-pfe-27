package com.adria.accountservice.service;
import com.adria.accountservice.service.AccountDtos.*;
import java.util.List;import java.util.UUID;
public interface AccountService {
 AccountView create(CreateAccount request);
 AccountView find(UUID id);
 List<AccountView> list();
 AccountView status(UUID id,StatusUpdate status);
 AccountView debit(UUID id,Money money);
 AccountView credit(UUID id,Money money);
 void transfer(Transfer transfer);
}
