package com.adria.transactionservice.client;
import feign.RequestInterceptor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.web.client.RestClient;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Map;
@Configuration public class FeignAuthConfig {
 @Bean RequestInterceptor relayBearerToken(@Value("${bank.security.enabled:false}") boolean security,
   @Value("${SERVICE_TOKEN_URL:http://localhost:8085/realms/bank/protocol/openid-connect/token}") String url,
   @Value("${BANK_SERVICE_CLIENT_ID:bank-svc}") String client,
   @Value("${BANK_SERVICE_CLIENT_SECRET:}") String secret){
  return template->{
   String auth=null;
   if(RequestContextHolder.getRequestAttributes() instanceof ServletRequestAttributes a)auth=a.getRequest().getHeader("Authorization");
   if(auth!=null && auth.startsWith("Bearer ")){template.header("Authorization",auth);return;}
   if(security && !secret.isBlank()){
    String form="grant_type=client_credentials&client_id="+URLEncoder.encode(client,StandardCharsets.UTF_8)+"&client_secret="+URLEncoder.encode(secret,StandardCharsets.UTF_8);
    Map<?,?> result=RestClient.create().post().uri(url).contentType(MediaType.APPLICATION_FORM_URLENCODED).body(form).retrieve().body(Map.class);
    if(result!=null&&result.get("access_token")!=null)template.header("Authorization","Bearer "+result.get("access_token"));
   }
  };
 }
}
