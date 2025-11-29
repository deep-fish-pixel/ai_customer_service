<script lang="ts">
  import Menu from '@smui/menu';
  import List, { Item, Separator, Text } from '@smui/list';
  import Button, { Label } from '@smui/button';
  import StyleIcon from "../../../../icons/StyleIcon.svelte";
  import SizeIcon from "../../../../icons/SizeIcon.svelte";
  import NumberIcon from "../../../../icons/NumberIcon.svelte";
  import {chatMessageState} from "../../../../state/chatMessages.svelte";
  import {ImageRatioTypes} from "../../../../../constants";

  let menuStyle: Menu;
  let menuRatio: Menu;
  let menuNumber: Menu;
  let style = $state('');
  let number = $state(1);
  let ratio: keyof typeof ImageRatioTypes = $state("1:1");

  $effect(() => {
    chatMessageState.model[chatMessageState.model_type].task_extra['style'] = style;
    chatMessageState.model[chatMessageState.model_type].task_extra['size'] = ImageRatioTypes[ratio].size || ImageRatioTypes['1:1'].size;
    chatMessageState.model[chatMessageState.model_type].task_extra['ratio'] = ratio || '1:1';
    chatMessageState.model[chatMessageState.model_type].task_extra['n'] = number;
  });
</script>

<!-- 输入区域 -->
<div class="opts-image">
  <div class="opt">
    <Button onclick={() => menuStyle.setOpen(true)}>
      <StyleIcon />
      <Label>风格{style ? ':'+style : ''}</Label>
    </Button>
    <Menu bind:this={menuStyle}>
      <List>
        <Item onSMUIAction={() => (style = '人像写真')}>
          <Text>人像摄影</Text>
        </Item>
        <Item onSMUIAction={() => (style = '写实摄影')}>
          <Text>写实摄影</Text>
        </Item>
        <Item onSMUIAction={() => (style = '绘画流派')}>
          <Text>绘画流派</Text>
        </Item>
        <Item onSMUIAction={() => (style = '海报设计')}>
          <Text>海报设计</Text>
        </Item>
        <Item onSMUIAction={() => (style = '建筑室内设计')}>
          <Text>建筑室内设计</Text>
        </Item>
        <Item onSMUIAction={() => (style = '小说封面')}>
          <Text>小说封面</Text>
        </Item>
        <Item onSMUIAction={() => (style = '动漫游戏')}>
          <Text>动漫游戏</Text>
        </Item>
        <Item onSMUIAction={() => (style = '3D渲染')}>
          <Text>3D渲染</Text>
        </Item>
        <Item onSMUIAction={() => (style = '水墨画')}>
          <Text>水墨画</Text>
        </Item>
        <Item onSMUIAction={() => (style = '儿童绘画')}>
          <Text>儿童绘画</Text>
        </Item>
        <Item onSMUIAction={() => (style = '二次元')}>
          <Text>二次元</Text>
        </Item>
      </List>
    </Menu>
  </div>
  <div class="opt">
    <Button onclick={() => menuRatio.setOpen(true)}>
      <SizeIcon />
      <Label>尺寸{ratio ? ':'+ratio : ''}</Label>
    </Button>
    <Menu bind:this={menuRatio}>
      <List>
        <Item onSMUIAction={() => (ratio = '16:9')}>
          <Text>16:9</Text>
        </Item>
        <Item onSMUIAction={() => (ratio = '4:3')}>
          <Text>4:3</Text>
        </Item>
        <Item onSMUIAction={() => (ratio = '1:1')}>
          <Text>1:1</Text>
        </Item>
        <Item onSMUIAction={() => (ratio = '3:4')}>
          <Text>3:4</Text>
        </Item>
        <Item onSMUIAction={() => (ratio = '9:16')}>
          <Text>9:16</Text>
        </Item>
      </List>
    </Menu>
  </div>
  <div class="opt">
    <Button onclick={() => menuNumber.setOpen(true)}>
      <NumberIcon />
      <Label>张数{number ? ':'+number+'张' : ''}</Label>
    </Button>
    <Menu bind:this={menuNumber}>
      <List>
        <Item onSMUIAction={() => (number = 1)}>
          <Text>1</Text>
        </Item>
        <Item onSMUIAction={() => (number = 2)}>
          <Text>2</Text>
        </Item>
        <Item onSMUIAction={() => (number = 3)}>
          <Text>3</Text>
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