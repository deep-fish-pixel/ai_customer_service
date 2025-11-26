<script lang="ts">
  import Textfield from '@smui/textfield';
  import Button from '@smui/button';
  import type {Message,} from "../../../types/chat";
  import SendIcon from "../../../icons/SendIcon.svelte";
  import {onMount, tick} from "svelte";
  import {getRecentMessages} from "../../../utils/handleMessages";
  import StopIcon from "../../../icons/StopIcon.svelte";
  import {JsonSeperatorRegex} from "../../../../constants";
  import {chatMessageState} from "../../../state/chatMessages.svelte";
  import {sendChatMessageStream} from "../../../services/chatService";
  import {getUserId} from "../../../state/userState.svelte";
  import ModelTabs from "./ModelTabs.svelte";
  import ModelImageOpts from "./opts/ModelImageOpts.svelte";
  import ImageUploads from "./opts/ImageUploads.svelte";


  const { onScrollToBottom, onGetUserinfoLocal }: {onScrollToBottom: () => void, onGetUserinfoLocal: () => void} = $props();
  // 状态管理
  let inputContainer: HTMLElement;
  let disabled = $derived(!chatMessageState.query || !getUserId());
  let receiving = $state(false);
  // 停止接收消息流句柄
  let abortStream: () => void;

  const resize = () => {
    // fix Textfield bug
    inputContainer.querySelector('textarea')?.setAttribute('placeholder', '请输入您的问题...');
  }

  // 发送消息
  export const sendMessage = async (message?: string) => {
    if (message) {
      chatMessageState.query = message;
    }
    if (!chatMessageState.query.trim() || receiving) return;

    // 添加用户消息
    const userMessage: Message = {
      id: Date.now().toString(),
      content: chatMessageState.query.trim(),
      sender: 'user',
      task_status: -1,
      timestamp: new Date(),
    };

    // 最近4条消息
    const history = getRecentMessages(chatMessageState.messages, 20);

    chatMessageState.messages = [...chatMessageState.messages, userMessage];

    console.log('send========', chatMessageState.messages);

    // 创建临时机器人消息
    const botMessageId = (Date.now() + 1).toString();
    const botMessage: Message = {
      id: botMessageId,
      content: '',
      sender: 'bot',
      task_status: -1,
      timestamp: new Date(),
    };
    chatMessageState.messages = [...chatMessageState.messages, botMessage];

    // 清空输入框
    chatMessageState.query = '';

    // 滚动到底部
    await tick();

    // 接收消息
    receiving = true;

    try {
      debugger
      // 使用流式请求
      abortStream = sendChatMessageStream(
        userMessage.content,
        history,
        chatMessageState.task_type,
        chatMessageState.task_extra,
        (chunk) => {
          // 更新机器人消息内容
          // 任务类型
          if (chunk && chunk.match(/\{'extract_info':/)) {
            return;
          }

          if (chunk && chunk.match(/\{'(task_status|collect_info|collect_origin)':/)) {
            chunk = chunk.replace(/: None/g, ': null');
            const response = new Function('return ' + chunk)();

            if (!response || response.task_status === 0) {
              return;
            }

            response.query = response.query.replace(JsonSeperatorRegex.CALL_GET_USER_INFO, () => {
              // 触发调用接口
              onGetUserinfoLocal();
              return '';
            })

            const task_status = response.task_status;
            // 任务完成后结束任务类型
            if (task_status === 2) {
              chatMessageState.task_type = '';
            } else {
              chatMessageState.task_type = response.task_type;
            }

            chatMessageState.messages = chatMessageState.messages.map((msg, index) => {
              if (msg.id === botMessageId) {
                if(task_status >= 0) {
                  const lastMessage = chatMessageState.messages[index -1];

                  if (lastMessage && !Number.isInteger(lastMessage.task_status)) {
                    lastMessage.task_status = 0;
                  }
                }
                return {
                  ...msg,
                  content: msg.content + response.query,
                  task_status: task_status,
                }
              }

              return msg;
            });

            console.log('receive===========1', chatMessageState.messages);
          } else {
            chatMessageState.messages = chatMessageState.messages.map(msg =>
              msg.id === botMessageId ? {...msg, content: msg.content + chunk} : msg
            );
            console.log('receive===========2', chatMessageState.messages);
          }

          onScrollToBottom();
        },
        () => {
          // 流结束
          receiving = false;
          onScrollToBottom();
        },
        (error) => {
          // 处理错误
          chatMessageState.messages = chatMessageState.messages.map(msg =>
            msg.id === botMessageId ? {
              ...msg,
              content: msg.content + (error.message.match(/aborted/) ? ' 该请求被取消' : ` 请求错误: ${error.message}`),
              sender: 'bot'
            } : msg
          );

          receiving = false;
          onScrollToBottom();
        }
      );
    } catch (error) {
      chatMessageState.messages = chatMessageState.messages.map(msg =>
        msg.id === botMessageId ? {
          ...msg,
          content: '连接服务器失败，请稍后重试',
          sender: 'bot'
        } : msg
      );
      receiving = false;
      onScrollToBottom();
    }

    // 提供取消功能
    return () => abortStream && abortStream();
  };

  const stopReceiveMessage = async () => {
    receiving = false;
    abortStream();
  }

  // 处理输入框回车事件
  const handleKeyPress = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey && !disabled) {
      e.preventDefault();
      sendMessage();
    }
  };

  // 工具切换处理
  const handleFocus = (focused: boolean) => {
    tick().then(() => resize());
  };

  onMount(() => {
    resize();
  });
</script>

<!-- 输入区域 -->
<div class="input-container">
  <ModelTabs />
  <div class="input-wrapper" bind:this={inputContainer}>
    <ImageUploads />
    <Textfield
        class="input-focus"
        textarea={true}
        variant="outlined"
        value={chatMessageState.query}
        oninput={(e) => chatMessageState.query = (e.target as HTMLInputElement)?.value}
        onkeydown={handleKeyPress}
        onfocus={() => handleFocus(true)}
        onfocusout={() => handleFocus(false)}
        placeholder="请输入您的问题..."
    />
    {#if receiving}
      <Button
          class="send-button"
          color="primary"
          onclick={stopReceiveMessage}
          title="取消接收消息"
      >
        <StopIcon></StopIcon>
      </Button>
    {:else}
      <Button
          class="send-button"
          color="primary"
          onclick={() => sendMessage()}
          disabled={disabled}
          title="发送消息"
      >
        <SendIcon></SendIcon>
      </Button>
    {/if}
  </div>
  <div class="opts">
    <ModelImageOpts />
  </div>
</div>
<style lang="scss">
  .input-container {
    background-color: #f5f5f5;
  }

  .input-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    position: relative;
    background-color: #fff;
    //box-shadow:  3px 3px 6px 6px #ddd;

    :global(.input-focusout) {
      width: 100%;
      height: 56px;

      :global(textarea) {
        resize: none;
      }
    }

    :global(.input-focus) {
      width: 100%;
      height: 100px;
      border:none;

      :global(textarea) {
        resize: none;
        width: 100%;
      }

      :global(.mdc-notched-outline){
        display: none;
      }
    }

    :global(.mdc-text-field__resizer) {
      width: 100%;
      resize: none;
    }

    :global(.mdc-notched-outline__leading) {
      border-width: 1px;
    }

    :global(.mdc-notched-outline__trailing) {
      border-width: 1px;
    }

    :global(.send-button) {
      min-width: 44px;
      overflow: hidden;
      padding: 0;
      margin: 0;
      outline: none;
      border: none;
      position: absolute;
      right: 0;
      bottom: 8px;
    }
  }

  .opts{
    background: #fff;
  }
</style>