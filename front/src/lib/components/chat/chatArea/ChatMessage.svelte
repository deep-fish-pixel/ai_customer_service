<script lang="ts">
  import type { Message, } from "../../../types/chat";
  import ViewTable from "./views/ViewTable.svelte"
  import ViewImages from "./views/ViewImages.svelte"
  import {DataShowTypes} from "../../../../constants";
  import ViewVideos from "./views/ViewVideos.svelte";

  // 从父组件接收的属性
  let { message, scrollToBottom }: { message: Message, scrollToBottom:() => void } = $props();
</script>

<div class={`chat-message ${message.sender} ${message.data_type === 'table' ? ' chat-message-table' : ''}`}>
  <div>
    {#if message.content}
      {message.content}

      {#if message.data_type === DataShowTypes.Table.value}
        <ViewTable headers={message.data_value[0]} list={message.data_value[1]} prevContent={message.content} />
      {/if}

      {#if message.data_type === DataShowTypes.Images.value}
        <ViewImages list={message.data_value} taskExtra={message.task_extra} />
      {/if}

      {#if message.data_type === DataShowTypes.Videos.value}
        <ViewVideos list={message.data_value} taskExtra={message.task_extra} scrollToBottom={scrollToBottom} />
      {/if}
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
    padding: 16px;
    margin-bottom: 20px;
    border-radius: 18px;
    max-width: 72%;
    word-wrap: break-word;
    clear: both;
  }

  .chat-message-table{
    max-width: 80%;
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
    margin-left: 8px;
    margin-right: auto;
    border-top-left-radius: 5px;
  }

  /* 发送的消息（自己）—— 右侧，绿色 */
  .user {
    background-color: #8984FF;
    align-self: flex-end;
    margin-left: auto;
    margin-right: 8px;
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