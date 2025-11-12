<script lang="ts">
  import List, {
    Item,
    Meta,
    Text,
    PrimaryText,
    SecondaryText,
  } from '@smui/list';
  import type {ToolConfig} from "../../types";

  // 从父组件接收的属性
  export let tools: ToolConfig[] = [];
  export let onToolOperate: (message?: string) => void;


  // 工具
  const demoTools: ToolConfig[] = [
    {
      id: 'schedule_meeting',
      name: '日程会议',
      description: '便捷创建、查询和管理您的日程会议，高效规划团队协作时间',
      questions: {
        question: '帮我创建日程会议',
        query: '查询我的日程会议记录',
      },
    },
    {
      id: 'leave_request',
      name: '请假申请',
      description: '轻松提交请假申请并查询审批状态，简化人事管理流程',
      questions: {
        question: '帮我创建请假申请',
        query: '查询我的请假申请记录',
      }
    },
    {
      id: 'flight_booking',
      name: '预定机票',
      description: '智能搜索并预订国内外航班，支持行程管理和退改签操作',
      questions: {
        question: '帮我预定机票',
        query: '查询我的预定机票记录',
      }
    },
    {
      id: 'hotel_booking',
      name: '预定酒店',
      description: '一键预订全球酒店，享受会员优惠价，灵活管理入住信息',
      questions: {
        question: '帮我预定酒店',
        query: '查询我的预定酒店记录',
      }
    },
    {
      id: 'change_nickname',
      name: '修改昵称',
      description: '个性化您的账户昵称，展现独特身份标识',
      questions: {
        question: '修改我的昵称',
      }
    },

  ];

  // 如果没有传入工具数据，使用演示数据
  $: displayTools = tools.length > 0 ? tools : demoTools;
</script>

<div class="tools-tab">
  <div class="tools-list">
    <List class="file-list">
      {#each displayTools as tool}
        <Item class="file-item" nonInteractive>
          <Text>
            <PrimaryText>{tool.name}</PrimaryText>
            <SecondaryText>{tool.description}</SecondaryText>
          </Text>
          <div class="tool-opts">
            {#if tool.questions?.question}
              <Meta class="material-icons" onclick={() => onToolOperate(tool.questions?.question)}>提问</Meta>
            {/if}
            {#if tool.questions?.query}
              <Meta class="material-icons" onclick={() => onToolOperate(tool.questions?.query)}>查询</Meta>
            {/if}
          </div>
        </Item>
      {/each}
    </List>
  </div>
</div>

<style lang="scss">
  :global(.MuiListItem-root) {
    border-radius: 8px;
    margin-bottom: 8px;
    transition: background-color 0.2s;

    &:hover {
      background-color: rgba(0, 0, 0, 0.04);
    }
  }

  .tools-tab{
    height: 100%;
    padding: 16px;

    .tool-opts{
      width: 84px;
      text-align: right;
    }

    :global(.file-list) {
      flex: 1;
      overflow-y: auto;
      padding: 0;
    }
    :global(.file-item){
      height: 66px;
      padding: 0;
      margin-bottom: 10px;
    }
    :global(.material-icons){
      color: var(--mdc-text-button-label-text-color, var(--mdc-theme-primary, #6200ee));
      cursor: pointer;
      font-size: 14px;
    }
    :global(.mdc-deprecated-list-item__text){
      white-space: normal;
      text-overflow: ellipsis;
      overflow: initial;
      word-wrap: break-word;
      flex: 1;
    }
    :global(.mdc-deprecated-list-item__secondary-text){
      font-size: 12px;
      white-space: normal;
    }
    :global(.mdc-deprecated-list-item__primary-text){
      font-size: 18px;
    }
  }
</style>