<script lang="ts">
  import type { Message, } from "../types/chat";
  import ViewTable from "./view/ViewTable.svelte"
  import {JsonSeperatorRegex} from "../../constants";

  function isSimpleType(data: any){
    return !data || typeof data === 'string' || typeof data === 'number' || typeof data === 'boolean';
  }

  function getData(content: string){
    const list = content && content.split(JsonSeperatorRegex.TYPE_LIST) || [];

    return list.map(str => {
      return str.match(/^\[\[/) ? JSON.parse(str) : str;
    });
  }


  // 从父组件接收的属性
  let { message, }: { message: Message } = $props();

  let contents = $derived.by(() => {
    return getData(message.content)
  });

  // 格式化时间
  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('zh-CN', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };
</script>

<div class={`chat-message ${message.sender}`}>
  <div>
    {#if message.content}
      {#each contents as content}
          {#if isSimpleType(content)}
            {content}
          {:else}
            <ViewTable headers={content[0]} list={content[1]}></ViewTable>
          {/if}
      {/each}
    {:else}
      <!--等待标识-->
      <span class="loader">
        <span>.</span>
        <span>.</span>
        <span>.</span>
      </span>
    {/if}
  </div>
</div>

<style lang="scss">
  .chat-message {
    position: relative;
    padding: 12px 16px;
    margin-bottom: 20px;
    border-radius: 18px;
    max-width: 70%;
    word-wrap: break-word;
    clear: both;
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

  .bot {
    background-color: #ffffff;
    align-self: flex-start;
    margin-right: auto;
    border-top-left-radius: 5px;
  }

  /* 发送的消息（自己）—— 右侧，绿色 */
  .user {
    background-color: #8984FF;
    align-self: flex-end;
    margin-left: auto;
    border-top-right-radius: 5px;
  }

  /* 顶部小三角（接收消息） */
  .bot::before {
    content: '';
    position: absolute;
    top: 0;
    left: -5px;
    width: 0;
    height: 0;
    border-top: 6px solid transparent;
    border-bottom: 6px solid transparent;
    border-right: 8px solid #ffffff;
  }

  /* 顶部小三角（发送消息） */
  .user::before {
    content: '';
    position: absolute;
    top: 0;
    right: -5px;
    width: 0;
    height: 0;
    border-top: 6px solid transparent;
    border-bottom: 6px solid transparent;
    border-left: 8px solid #8984FF;
  }

  .loader {
    display: inline-block;
    animation: blink 1.5s infinite;
  }

  .loader span {
    display: inline-block;
    animation: fade 1.5s infinite;
  }

  .loader span:nth-child(2) {
    animation-delay: 0.5s;
  }

  .loader span:nth-child(3) {
    animation-delay: 1s;
  }

  @keyframes fade {
    0%, 100% { opacity: 0; }
    50% { opacity: 1; }
  }
</style>