<script lang="ts">
  import Textfield from '@smui/textfield';
  import Button, {Label} from '@smui/button';
  import Paper from '@smui/paper';
  import type {Message,} from "../../../types/chat";
  import SendIcon from "../../../icons/SendIcon.svelte";
  import {onMount, tick} from "svelte";
  import {getRecentMessages} from "../../../utils/handleMessages";
  import StopIcon from "../../../icons/StopIcon.svelte";
  import {JsonSeperatorRegex} from "../../../../constants";
  import {chatMessageState} from "../../../state/chatMessages.svelte";
  import {sendChatMessageStream} from "../../../services/chatService";
  import {getUserId} from "../../../state/userState.svelte";



</script>

<!-- 输入区域 -->
<div class="tabs-box">
  <div class="tabs">
    <div class="tab tab1 active-prev">文本对话</div>
    <div class="tab tab2 active">图片生成</div>
    <div class="tab tab3 ">视频生成</div>
  </div>
</div>
<style lang="scss">
  .tabs-box{
    position: relative;
    z-index: 1;
  }
  .tabs{
    position: relative;
    z-index: 0;
    display: flex;
    //box-shadow:  -3px -3px 3px 3px #ddd;
    width: 450px;
  }
  .tab{
    width: 167px;
    height: 38px;
    line-height: 38px;
    position: relative;
    color: rgba(0, 0, 0, 0.87);
    font-size: 15px;
    margin-right: -14px;
    text-align: center;
    cursor: pointer;
  }
  .tab::after{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 167px;
    height: 100%;
    background-color: #ddd;
    border-radius: 8px 8px 0 0;
    transform: skewX(15deg);
    z-index: -1;
  }

  .active{
    color: #726cf8;
  }
  .active::after{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 167px;
    height: 100%;
    background-color: #fff;
  }
  .tab1::before{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 150px;
    height: 100%;
    background-color: #ddd;
    z-index: -2;
    border-radius: 10px 0 0 0;
  }
  .tab1::after{
    width: 157px;
    left: 10px;
  }
  .tab1.active::before{
    background-color: #fff;
  }
  .tab.active{
    border-bottom: 0 !important;
    z-index: 2;
  }
  .tab.active::before{
    height: 100%;
  }
  .tab.active::after{
    height: 100%;
  }
  .tab.active-prev{
    z-index: 3;
  }
</style>