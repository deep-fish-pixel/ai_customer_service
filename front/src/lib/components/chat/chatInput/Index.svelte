<script lang="ts">
  import Textfield from '@smui/textfield';
  import Button from '@smui/button';
  import type {Message,} from "../../../types/chat";
  import SendIcon from "../../../icons/SendIcon.svelte";
  import {onMount, tick} from "svelte";
  import {getRecentMessages} from "../../../utils/handleMessages";
  import StopIcon from "../../../icons/StopIcon.svelte";
  import {chatMessageState} from "../../../state/chatMessages.svelte";
  import {sendChatMessageStream} from "../../../services/chatService";
  import {getUserId} from "../../../state/userState.svelte";
  import ModelTabs from "./ModelTabs.svelte";
  import ModelImageOpts from "./opts/ModelImageOpts.svelte";
  import ImageUploads from "./opts/ImageUploads.svelte";
  import {DataShowTypes, ModelTypes} from "../../../../constants";
  import ModelVideoOpts from "./opts/ModelVideoOpts.svelte";


  const { onScrollToBottom, onGetUserinfoLocal }: {onScrollToBottom: () => void, onGetUserinfoLocal: (message: Message) => void} = $props();

  const callMethods = {
    getUserinfo: onGetUserinfoLocal,
  };
  // 状态管理
  let inputContainer: HTMLElement;
  let disabled = $derived(!chatMessageState.model[chatMessageState.model_type].query || !getUserId());
  let receiving = $state(false);
  // 停止接收消息流句柄
  let abortStream: () => void;

  const getInputPlaceholder = () => {
    switch (chatMessageState.model_type) {
      case ModelTypes.Text.value:
        return '请输入您的问题...';
      case ModelTypes.Image.value:
        return '支持图像生成与编辑，快速实现创意设计';
      case ModelTypes.Video.value:
        return '支持视频生成与编辑，快速实现创意设计';
      default:
        return '请输入您的问题...';
    }
  };

  const resize = () => {
    // fix Textfield bug
    const placeholder = getInputPlaceholder();
    inputContainer.querySelector('textarea')?.setAttribute('placeholder', placeholder);

  }

  $effect(() => {
    resize();
  });

  //

  // 发送消息
  export const sendMessage = async (message?: string) => {
    if (message) {
      chatMessageState.model[chatMessageState.model_type].query = message;
    }
    if (!chatMessageState.model[chatMessageState.model_type].query.trim() || receiving) return;

    const task_extra = chatMessageState.model[chatMessageState.model_type].task_extra;

    // 添加用户消息
    const userMessage: Message = {
      id: Date.now().toString(),
      content: chatMessageState.model[chatMessageState.model_type].query.trim(),
      sender: 'user',
      task_status: -1,
      data_type: chatMessageState.task_type === ModelTypes.Image.taskType ? DataShowTypes.Images.value : '',
      data_value: (task_extra.images || []).map(image => ({image: image})),
      timestamp: new Date(),
    };

    // 最近4条消息
    const history = getRecentMessages(chatMessageState.messages, 20);

    chatMessageState.messages = [...chatMessageState.messages, userMessage];

    // 创建临时机器人消息
    const botMessageId = (Date.now() + 1).toString();
    const botMessage: Message = {
      id: botMessageId,
      content: chatMessageState.task_type === ModelTypes.Image.taskType ? chatMessageState.model[chatMessageState.model_type].task_extra.images?.length ? '图片正在编辑中...' : '图片正在生成中...' : '',
      sender: 'bot',
      task_status: -1,
      data_type: chatMessageState.task_type === ModelTypes.Image.taskType ? DataShowTypes.Images.value : '',
      data_value: chatMessageState.task_type === ModelTypes.Image.taskType ? [...Array(chatMessageState.model[chatMessageState.model_type].task_extra.n)].map(() => ({image: ''})) : [],
      timestamp: new Date(),
    };

    chatMessageState.messages = [...chatMessageState.messages, botMessage];


    // 清空输入框
    chatMessageState.model[chatMessageState.model_type].query = '';

    // 滚动到底部
    await tick();

    // 接收消息
    receiving = true;

    let firstReceive = true;

    try {
      // 使用流式请求
      abortStream = sendChatMessageStream(
        userMessage.content,
        history,
        chatMessageState.task_type,
        chatMessageState.model[chatMessageState.model_type].task_extra,
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

            const task_status = response.task_status;
            // 任务完成后结束任务类型
            if (task_status === 2) {
              if (chatMessageState.model_type === ModelTypes.Text.value) {
                chatMessageState.task_type = '';
              }
            } else {
              chatMessageState.task_type = response.task_type;
            }

            if (response.data_value) {
              response.data_value = JSON.parse(response.data_value);
            }


            let delayCallMethod: (message: Message) => void;

            if (response.data_type === 'call') {
              const method: (...args: Array<any>) => void = callMethods[response.data_value.name as keyof typeof callMethods]

              delayCallMethod = (message: Message) => {
                try{
                  method.apply(null, [message, ...response.data_value.params]);
                }catch (e) {
                  console.error(e);
                }
              };
            }

            chatMessageState.messages = chatMessageState.messages.map((msg, index) => {
              if (msg.id === botMessageId) {
                if(task_status >= 0) {
                  const lastMessage = chatMessageState.messages[index -1];

                  if (lastMessage && !Number.isInteger(lastMessage.task_status)) {
                    lastMessage.task_status = 0;
                  }
                }

                if (firstReceive) {
                  msg.content = '';
                }

                const message: Message = {
                  ...msg,
                  content: msg.content + response.query,
                  data_type: response.data_type,
                  data_value: response.data_value,
                  task_status: task_status,
                  task_extra: chatMessageState.model[chatMessageState.model_type].task_extra,
                }

                // 触发调用接口
                delayCallMethod && delayCallMethod(message);

                if (response.data_type) {
                  // 动态数据延迟滚动
                  setTimeout(() => {
                    onScrollToBottom();
                  }, 100);
                }

                return  message;
              }

              return msg;
            });

          } else {
            chatMessageState.messages = chatMessageState.messages.map(msg =>
              msg.id === botMessageId ? {...msg, content: msg.content + chunk} : msg
            );
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

      if (task_extra?.images?.length) {
        if (chatMessageState.model[chatMessageState.model_type].task_extra) {
          // 重置images
          task_extra.images = [];
        }
      }
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

    setTimeout(() => {
      onScrollToBottom();
    }, 100);

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
    {#if chatMessageState.model_type !== ModelTypes.Text.value}
      <ImageUploads />
    {/if}
    <Textfield
        class="input-focus"
        textarea={true}
        variant="outlined"
        value={chatMessageState.model[chatMessageState.model_type].query}
        oninput={(e) => chatMessageState.model[chatMessageState.model_type].query = (e.target as HTMLInputElement)?.value}
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
    {#if chatMessageState.model_type === ModelTypes.Image.value}
      <ModelImageOpts />
    {/if}
    {#if chatMessageState.model_type === ModelTypes.Video.value}
      <ModelVideoOpts />
    {/if}
  </div>
</div>
<style lang="scss">
  .input-container {
    background-color: transparent;
    position: relative;
  }

  .input-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    position: relative;
    background-color: #fff;
    //box-shadow:  3px 3px 6px 6px #ddd;

    :global(.input-focus) {
      width: 100%;
      height: 100px;
      border:none;

      :global(textarea) {
        resize: none;
        width: 100%;
        margin-top: 10px;
        margin-bottom: 2px;
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
    height: 36px;
    background: #fff;
  }
</style>