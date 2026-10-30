package com.adria.gatewayservice;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.reactive.CorsConfigurationSource;
import org.springframework.web.cors.reactive.UrlBasedCorsConfigurationSource;
import java.util.List;
@Configuration public class GatewaySecurity {
 @Bean SecurityWebFilterChain gatewayChain(ServerHttpSecurity http,@Value("${bank.security.enabled:false}") boolean enabled){
  http.csrf(ServerHttpSecurity.CsrfSpec::disable).cors(cors -> {});
  if(enabled){http.authorizeExchange(e->e.pathMatchers("/actuator/health/**").permitAll().anyExchange().authenticated()).oauth2ResourceServer(o->o.jwt(j->{}));}
  else{http.authorizeExchange(e->e.anyExchange().permitAll());}
  return http.build();
 }
 @Bean CorsConfigurationSource cors(){
  CorsConfiguration c=new CorsConfiguration(); c.setAllowedOrigins(List.of("http://localhost:4200"));
  c.setAllowedMethods(List.of("GET","POST","PUT","PATCH","DELETE","OPTIONS"));c.setAllowedHeaders(List.of("Authorization","Content-Type"));
  UrlBasedCorsConfigurationSource s=new UrlBasedCorsConfigurationSource();s.registerCorsConfiguration("/**",c);return s;
 }
}
