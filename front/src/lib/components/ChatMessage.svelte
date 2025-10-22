<script lang="ts">
  import Paper, { Content } from '@smui/paper';

  import type {Message} from "../../types";
  


  // 从父组件接收的属性
  export let message: Message;

  // 格式化时间
  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('zh-CN', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };
</script>

<div class={`chat-message ${message.sender}`}>
  <Paper 
    elevation={1} 
    class="message-bubble"
  >
    <!--style={{
      backgroundColor: message.sender === 'user' ? '#e3f2fd' : '#ffffff',
      borderRadius: '12px',
      maxWidth: '70%'
    }}-->
    <Content class="message-content">
      {message.content}
    </Content>
    <Content class="message-time">
      {formatTime(message.timestamp)}
    </Content>
  </Paper>
</div>

<style lang="scss">
  .chat-message {
    display: flex;
    margin-bottom: 16px;
    padding: 0 16px;

    &.user {
      justify-content: flex-end;
    }

    &.bot {
      justify-content: flex-start;
    }
  }

  .message-bubble {
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
  }

  .message-content {
    word-wrap: break-word;
    white-space: pre-wrap;
    margin-bottom: 4px;
  }

  .message-time {
    align-self: flex-end;
    opacity: 0.6;
  }
</style>