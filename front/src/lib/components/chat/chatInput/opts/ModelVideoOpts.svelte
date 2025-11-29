<script lang="ts">
  import Menu from '@smui/menu';
  import List, { Item, Separator, Text } from '@smui/list';
  import Button, { Label } from '@smui/button';
  import ResolutionIcon from "../../../../icons/ResolutionIcon.svelte";
  import DurationIcon from "../../../../icons/DurationIcon.svelte";
  import {chatMessageState} from "../../../../state/chatMessages.svelte";

  let menuResolution: Menu;
  let menuDuration: Menu;
  let resolution = $state('480P');
  let duration = $state(5);

  $effect(() => {
    chatMessageState.model[chatMessageState.model_type].task_extra['resolution'] = resolution;
    chatMessageState.model[chatMessageState.model_type].task_extra['duration'] = duration = 5;
  });
</script>

<!-- 输入区域 -->
<div class="opts-image">
  <div class="opt">
    <Button onclick={() => menuResolution.setOpen(true)}>
      <ResolutionIcon />
      <Label>分辨率{resolution ? ':'+resolution : ''}</Label>
    </Button>
    <Menu bind:this={menuResolution}>
      <List>
        <Item onSMUIAction={() => (resolution = '480P')}>
          <Text>480P</Text>
        </Item>
        <Item onSMUIAction={() => (resolution = '720P')}>
          <Text>720P</Text>
        </Item>
      </List>
    </Menu>
  </div>
  <div class="opt">
    <Button onclick={() => menuDuration.setOpen(true)}>
      <DurationIcon />
      <Label>时长{duration ? ':'+duration + 's' : ''}</Label>
    </Button>
    <Menu bind:this={menuDuration}>
      <List>
        <Item onSMUIAction={() => (duration = 5)}>
          <Text>5s</Text>
        </Item>
        <Item onSMUIAction={() => (duration = 10)}>
          <Text>10s</Text>
        </Item>
      </List>
    </Menu>
  </div>
</div>
<style lang="scss">
  .opts-image{
    display: flex;

    .opt{
      min-width: 60px;
      margin-right: 20px;

      &:first-child{
        margin-left: 8px;
      }

      :global(.mdc-button){
        color: #424242;
        outline: none;
        border: 1px solid #eee;

        :global(svg){
          margin-right: 4px;
        }
      }
    }
  }
</style>