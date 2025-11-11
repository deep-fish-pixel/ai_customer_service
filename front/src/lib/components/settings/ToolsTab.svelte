<script lang="ts">
  import Card, { Content } from '@smui/card';
  import Switch from '@smui/switch';
  import Paper, { Title } from '@smui/paper';
  import type {ToolConfig} from "../../types";
  


  // 从父组件接收的属性
  export let tools: ToolConfig[] = [];
  export let onToolToggle: (toolId: string, enabled: boolean) => void;

  // 工具
  const demoTools: ToolConfig[] = [
    {
      id: 'schedule_meeting',
      name: '日程会议',
      description: '提供日程会议的新建和查询',
    },
    {
      id: 'leave_request',
      name: '请假申请',
      description: '提供请假申请的新建和查询',
    },
    {
      id: 'flight_booking',
      name: '预定机票',
      description: '提供预定机票的新建和查询',
    },
    {
      id: 'hotel_booking',
      name: '预定酒店',
      description: '提供预定酒店的新建和查询',
    },
    {
      id: 'change_nickname',
      name: '修改昵称',
      description: '修改我的昵称',
    },

  ];

  // 如果没有传入工具数据，使用演示数据
  $: displayTools = tools.length > 0 ? tools : demoTools;
</script>

<div class="tools-tab">
  <div class="tools-list">
    {#each displayTools as tool}
      <div class="tool-item">
        <div class="tool-header">
          <div class="tool-info">
            <div class="tool-name">{tool.name}</div>
            <div class="textSecondary">{tool.description}</div>
          </div>
          <div>
            <div>开始</div>
            <div>查询</div>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>

<style lang="scss">
  .tools-tab {
    height: 100%;
    padding: 16px;
  }

  .tools-container {
    height: 100%;
    padding: 16px;
    display: flex;
    flex-direction: column;
  }

  .section-title {
    margin-bottom: 16px;
    color: rgba(0, 0, 0, 0.87);
  }

  .tools-list {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 12px;
    overflow-y: auto;
    padding-bottom: 16px;
  }

  .tool-item {
    border-radius: 8px;
    overflow: hidden;
  }

  .tool-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .tool-info {
    flex: 1;
    margin-right: 16px;
  }

  .tool-name {
    font-weight: 500;
    margin-bottom: 4px;
  }

  .coming-soon {
    margin-top: auto;
    text-align: center;
    background-color: #f5f5f5;
    border-radius: 8px;
  }
</style>