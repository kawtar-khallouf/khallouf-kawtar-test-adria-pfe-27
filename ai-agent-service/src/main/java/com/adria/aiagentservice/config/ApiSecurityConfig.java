package com.adria.aiagentservice.config;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;
import java.util.List;
@Configuration @EnableMethodSecurity
public class ApiSecurityConfig {
 @Bean SecurityFilterChain apiSecurity(HttpSecurity http, @Value("${bank.security.enabled:false}") boolean enabled) throws Exception {
  http.csrf(csrf -> csrf.disable()).cors(cors -> {}).sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
  if (enabled) {
   http.authorizeHttpRequests(a -> a
     .requestMatchers("/actuator/health/**","/v3/api-docs/**","/swagger-ui/**","/h2-console/**").permitAll()
     // MCP is network-internal only in Docker; do not publish it directly in production.
     .requestMatchers("/sse","/mcp/message").permitAll()
     .anyRequest().authenticated()).oauth2ResourceServer(o -> o.jwt(j -> {}));
  } else { http.authorizeHttpRequests(a -> a.anyRequest().permitAll()); }
  http.headers(h -> h.frameOptions(f -> f.sameOrigin()));
  return http.build();
 }
 @Bean CorsFilter apiCors() {
  CorsConfiguration c=new CorsConfiguration();
  c.setAllowedOrigins(List.of("http://localhost:4200"));
  c.setAllowedMethods(List.of("GET","POST","PUT","PATCH","DELETE","OPTIONS"));
  c.setAllowedHeaders(List.of("Authorization","Content-Type"));
  UrlBasedCorsConfigurationSource source=new UrlBasedCorsConfigurationSource();
  source.registerCorsConfiguration("/**",c);
  return new CorsFilter(source);
 }
}
