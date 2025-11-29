<script lang="ts">
  import Menu from '@smui/menu';
  import List, { Item, Text } from '@smui/list';
  import Button, { Label } from '@smui/button';
  import DurationIcon from "../../../../icons/DurationIcon.svelte";
  import {chatMessageState} from "../../../../state/chatMessages.svelte";
  import SizeIcon from "../../../../icons/SizeIcon.svelte";
  import {VideoRatioTypes} from "../../../../../constants";

  let menuRatio: Menu;
  let menuDuration: Menu;
  let ratio: keyof typeof VideoRatioTypes = $state("1:1");
  let duration = $state(5);

  $effect(() => {
    chatMessageState.model[chatMessageState.model_type].task_extra['duration'] = duration = 5;
    chatMessageState.model[chatMessageState.model_type].task_extra['size'] = VideoRatioTypes[ratio].size || VideoRatioTypes['1:1'].size;

  });
</script>

<!-- 输入区域 -->
<div class="opts-image">
  <div class="opt">
    <Button onclick={() => menuRatio.setOpen(true)}>
      <SizeIcon />
      <Label>尺寸{ratio ? ':'+ ratio : ''}</Label>
    </Button>
    <Menu bind:this={menuRatio}>
      <List>
        <Item onSMUIAction={() => (ratio = '16:9')}>
          <Text>16:9</Text>
        </Item>
        <Item onSMUIAction={() => (ratio = '1:1')}>
          <Text>1:1</Text>
        </Item>
        <Item onSMUIAction={() => (ratio = '9:16')}>
          <Text>9:16</Text>
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