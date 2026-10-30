package com.adria.aiagentservice;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import java.util.Arrays;
@RestController @RequestMapping("/api/chat")
public class AgentController {
 private final ChatClient client;private final ToolCallbackProvider tools;
 public AgentController(ChatClient.Builder builder,ToolCallbackProvider tools){
  this.client=builder.defaultSystem("You are a cautious banking assistant. Use MCP tools to verify real values. Never invent balances, account numbers or transaction success. Do not perform any write unless specifically permitted by the request. Never expose sensitive data unrelated to the query.").build();
  this.tools=tools;
 }
 public record ChatRequest(String message,boolean confirmWrites){}
 public record ChatAnswer(String answer){}
 @PostMapping public ChatAnswer chat(@RequestBody ChatRequest request){
  if(request.message()==null||request.message().isBlank())throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Message required");
  if(request.message().length()>1500)throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Message too long");
  ToolCallback[] allowed=Arrays.stream(tools.getToolCallbacks()).filter(t->request.confirmWrites() || !(t.getToolDefinition().name().contains("registerBankTransaction")||t.getToolDefinition().name().contains("executeBankTransfer"))).toArray(ToolCallback[]::new);
  String result=client.prompt().user(request.message()).toolCallbacks(allowed).call().content();
  return new ChatAnswer(result==null?"No response":result);
 }
}
