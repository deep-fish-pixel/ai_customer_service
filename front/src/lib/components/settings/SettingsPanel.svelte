<script lang="ts">
  import Tab, { Label } from '@smui/tab';
  import TabBar from '@smui/tab-bar';
  import DocumentsTab from './DocumentsTab.svelte';
  import ToolsTab from './ToolsTab.svelte';
  import type {FileItem, ToolConfig} from "../../types";

  // 标签页类型
  type TabValue = '个人知识库' | '高效工具';

  // 状态管理
  let activeTab: TabValue = '个人知识库';

  // 从父组件接收的属性
  export let tools: ToolConfig[] = [];
  export let onToolToggle: (toolId: string, enabled: boolean) => void;
</script>

<div class="settings-panel">
  <!-- 标签页 -->
  <TabBar
    tabs={['个人知识库', '工具']}
    bind:active={activeTab}
  >
    {#snippet tab(tab)}
      <Tab {tab}>
        <Label>{tab}</Label>
      </Tab>
    {/snippet}
  </TabBar>

  <!-- 标签页内容 -->
  <div class="tab-content">
    {#if activeTab === '个人知识库'}
      <DocumentsTab/>
    {/if}
    
    {#if activeTab === '工具'}
      <ToolsTab
        {tools}
        {onToolToggle}
      />
    {/if}
  </div>
</div>

<style lang="scss">
  .settings-panel {
    height: 100%;
    display: flex;
    flex-direction: column;
    background-color: #ffffff;
  }

  :global(.MuiTabs-root) {
    border-bottom: 1px solid #e0e0e0;
  }

  :global(.MuiTab-root) {
    text-transform: none;
    font-size: 14px;
    font-weight: 500;
  }

  :global(.Mui-selected) {
    color: #1976d2 !important;
  }

  .tab-content {
    flex: 1;
    overflow: hidden;
  }
</style>