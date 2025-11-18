<script lang="ts">
  import Tab, { Label } from '@smui/tab';
  import TabBar from '@smui/tab-bar';
  import DocumentsTab from './DocumentsTab.svelte';
  import ToolsTab from './ToolsTab.svelte';
  import HideShowIcon from './HideShowIcon.svelte';

  // 标签页类型
  type TabValue = '个人知识库' | '提效工具';

  // 状态管理
  let activeTab: TabValue = $state('个人知识库');

  let expanded = $state(window.screen.width > 768);


  const iconClickHandle = (isHide: boolean) => {
    expanded = isHide;
  };

  const { onToolOperate, } = $props();
</script>

<div class={'settings-container' + (expanded?'':' settings-container-hide')}>
  <div class="settings-bg" onclick={() => iconClickHandle(false)}></div>
  <div class="settings-panel">
    <div class="settings-header">
      <p class="settings-title">模型设置</p>
      <HideShowIcon class="settings-icon" value={expanded} onClick={iconClickHandle} />
    </div>
    <!-- 标签页 -->
    <TabBar
      class="settings-tab-bar"
      tabs={['个人知识库', '提效工具']}
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

      {#if activeTab === '提效工具'}
        <ToolsTab
          onToolOperate={onToolOperate}
        />
      {/if}
    </div>
  </div>
</div>
<style lang="scss">
  .settings-container{
    position: relative;
  }
  .settings-bg {
    height: 100%;
    width: 100%;
    position: absolute;
    background-color: rgba(0, 0, 0, 0.1);
  }
  .settings-panel {
    width: 350px;
    height: 100%;
    display: flex;
    flex-direction: column;
    background-color: #ffffff;
    border-left: 1px solid var(--boxBorderColor);
    position: relative;
  }

  @media screen and (max-width: 768px) {
    .settings-container{
      width: 100%;
      height: calc(100% - 54px);
      position: absolute;
      top: 0;
      right: 0;
      z-index: 1;
      padding-top: 54px;
      display: grid;
      justify-items: end;
    }
    .settings-panel {
      width: 280px;
    }
  }

  @media screen and (min-width: 768px) and (max-width: 1024px) {
    .settings-container{
      width: 100%;
      height: calc(100% - 54px);
      position: absolute;
      top: 0;
      right: 0;
      z-index: 1;
      padding-top: 54px;
      display: grid;
      justify-items: end;
    }
    .settings-panel {
      width: 320px;
    }
  }

  .settings-container-hide{
    width: 0;

    .settings-bg{
      display: none;
    }
    .settings-panel{
      width: 0;
      min-width: 0;
      max-width: 0;

      :global(.settings-title){
        display: none;
      }
    }
  }



  :global(.settings-icon){
    position: absolute;
    top: 0;
    right: 0;
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

  .settings-header{
    height: 48px;
    display: flex;
    flex-direction: row;

    .settings-title{
      flex: 1;
      font-size: 1rem;
      line-height: 1.2rem;
      margin-left: 10px;
    }
  }
</style>