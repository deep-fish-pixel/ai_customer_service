<script lang="ts">
  import TextIcon from "../../../icons/TextIcon.svelte";
  import ImageIcon from "../../../icons/ImageIcon.svelte";
  import VideoIcon from "../../../icons/VideoIcon.svelte";
  import {chatMessageState} from "../../../state/chatMessages.svelte";
  import {ModelTypes} from "../../../../constants";

  const tabs = [ModelTypes.Text, ModelTypes.Image, ModelTypes.Video, ];
  let modelIndex = $state(0);

  chatMessageState.task_type = tabs[0].taskType

  $effect(() => {
    tabs.some((tab,index) => {
      if(tab.value === chatMessageState.model_type){
        modelIndex = index;
        return true;
      }
    });
  });

  const clickHandle = (index: number) => {
    chatMessageState.model_type = tabs[index].value;
    chatMessageState.task_type = tabs[index].taskType
  }
</script>

<!-- 输入区域 -->
<div class="tabs-box">
  <div class="tabs">
    {#each tabs as tab, index}
      <div
        class={"tab" + (modelIndex === index ? " active" : modelIndex - 1 === index ? " active-prev" : "")}
        onclick={() => clickHandle(index)}>
        {#if index===0}
          <TextIcon />
        {:else if index===1}
          <ImageIcon />
        {:else if index===2}
          <VideoIcon />
        {/if}
        <span class="name">{tab.lable}</span>
      </div>
    {/each}
  </div>
</div>
<style lang="scss">
  .tabs-box{
    position: absolute;
    z-index: 1;
    top: -38px;
  }
  .tabs{
    position: relative;
    z-index: 0;
    display: flex;
    font-weight: 600;
    //box-shadow:  -3px -3px 3px 3px #ddd;
    width: 450px;
    margin-left: 14px;
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
    display: flex;
    align-items: center;
    justify-content: center;

    span{
      margin-left: 4px;
    }

    &:nth-child(2){
      span{
        margin-left: 0;
      }
    }

    &:first-child{
      &::before{
        content: "";
        position: absolute;
        top: 0;
        left: -9px;
        width: 150px;
        height: 100%;
        background-color: #ddd;
        z-index: -1;
        border-radius: 10px 0 0 0;
        transform: skewX(-15deg);
      }
      &::after{
        width: 157px;
        left: 10px;
      }
      &.active::before{
        background-color: #fff;
      }
    }
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
  .active::before{
    content: "";
    position: absolute;
    top: 0;
    left: -9px;
    width: 150px;
    height: 100%;
    background-color: #ffffff;
    z-index: -1;
    border-radius: 10px 0 0 0;
    transform: skewX(-15deg);
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

  @media screen and (max-width: 490px) {
    .tabs{
      width: 360px;
      .name{
        display: none;
      }
    }

    .tab{
      width: 120px;

      &:first-child{
        &::before{
          width: 120px;
        }
        &::after{
          width: 120px;
        }
      }
    }
    .tab::after{
      width: 120px;
    }

    .active::before{
      width: 90px;
    }
    .active::after{
      width: 120px;
    }
  }
</style>