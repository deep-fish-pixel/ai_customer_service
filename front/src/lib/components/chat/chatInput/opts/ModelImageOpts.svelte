<script lang="ts">
  import Menu from '@smui/menu';
  import List, { Item, Separator, Text } from '@smui/list';
  import Button, { Label } from '@smui/button';

  let menuStyle: Menu;
  let menuSize: Menu;
  let menuNumber: Menu;
  let clicked = $state('nothing yet');

</script>

<!-- 输入区域 -->
<div class="opts-image">
  <div class="opt">
    <Button onclick={() => menuStyle.setOpen(true)}>
      <Label>风格模型</Label>
    </Button>
    <Menu bind:this={menuStyle}>
      <List>
        <Item onSMUIAction={() => (clicked = 'Cut')}>
          <Text>Cut</Text>
        </Item>
        <Item onSMUIAction={() => (clicked = 'Copy')}>
          <Text>Copy</Text>
        </Item>
        <Item onSMUIAction={() => (clicked = 'Paste')}>
          <Text>Paste</Text>
        </Item>
        <Separator />
        <Item onSMUIAction={() => (clicked = 'Delete')}>
          <Text>Delete</Text>
        </Item>
      </List>
    </Menu>
  </div>
  <div class="opt">
    <Button onclick={() => menuSize.setOpen(true)}>
      <Label>图片尺寸</Label>
    </Button>
    <Menu bind:this={menuSize}>
      <List>
        <Item onSMUIAction={() => (clicked = 'Cut')}>
          <Text>Cut</Text>
        </Item>
        <Item onSMUIAction={() => (clicked = 'Copy')}>
          <Text>Copy</Text>
        </Item>
        <Item onSMUIAction={() => (clicked = 'Paste')}>
          <Text>Paste</Text>
        </Item>
        <Separator />
        <Item onSMUIAction={() => (clicked = 'Delete')}>
          <Text>Delete</Text>
        </Item>
      </List>
    </Menu>
  </div>
  <div class="opt">
    <Button onclick={() => menuNumber.setOpen(true)}>
      <Label>图片张数</Label>
    </Button>
    <Menu bind:this={menuNumber}>
      <List>
        <Item onSMUIAction={() => (clicked = 'Cut')}>
          <Text>Cut</Text>
        </Item>
        <Item onSMUIAction={() => (clicked = 'Copy')}>
          <Text>Copy</Text>
        </Item>
        <Item onSMUIAction={() => (clicked = 'Paste')}>
          <Text>Paste</Text>
        </Item>
        <Separator />
        <Item onSMUIAction={() => (clicked = 'Delete')}>
          <Text>Delete</Text>
        </Item>
      </List>
    </Menu>
  </div>
</div>
<style lang="scss">
  .opts-image{
    display: flex;

    .opt{
      :global(.mdc-button){
        color: #424242;
        outline: none;
        border: none;
      }
    }
  }
</style>