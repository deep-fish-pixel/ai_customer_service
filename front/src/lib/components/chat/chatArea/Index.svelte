<script lang="ts">
  import type {Message,} from "../../../types/chat";
  import {onMount, tick} from "svelte";
  import ChatMessage from "./ChatMessage.svelte";
  import {chatMessageState} from "../../../state/chatMessages.svelte";

  // 状态管理
  let messageContainer: HTMLElement;
  let height = $state(500);
  // 停止接收消息流句柄

  const resize = () => {
    height = window.innerHeight - 238 -6;
  };

  export const scrollToBottom = () => {
    if (messageContainer) {
      messageContainer.scrollTop = messageContainer.scrollHeight;
    }
  };

  window.addEventListener('resize', resize)

  onMount(() => {
    resize();
  });
</script>

<!-- 输入区域 -->
<div class="messages-container hide-scrollbar" style={"height:" + height + "px;"}
     bind:this={messageContainer}>
  <div class="messages">
    {#each chatMessageState.messages as message}
      <ChatMessage message={message}/>
    {/each}
  </div>
</div>
<style lang="scss">
  .messages-container {
    overflow-y: scroll;
    background-color: #f5f5f5;
    padding: 16px 0 28px 0;
  }

  .messages {
    display: flex;
    flex-direction: column;
  }

</style>