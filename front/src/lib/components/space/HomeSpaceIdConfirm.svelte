<script lang="ts">
    import Button, { Label } from '@smui/button';
    import Textfield from '@smui/textfield';
    import HelperText from '@smui/textfield/helper-text';
    import List, {
        Item,
        Meta,
        Text,
        PrimaryText,
        SecondaryText,
    } from '@smui/list';
    import type {DocumentFile} from "../../types/document";
    import Dialog, { Title, Content, Actions } from '@smui/dialog';


    const ButtonName = '上传知识库';
    let buttonName = ButtonName;
    let deleteVisible = $state(true);
    let forDeletedDocument:DocumentFile = $state({
        file_name: '',
        file_size: 0,
        upload_time: Date(),
    });

    let focused = $state(false);
    let value: string | null = $state(null);
    let dirty = $state(false);
    let invalid = $state(true);
    const disabled = $derived(focused || !value || !dirty || invalid);

    function handlerChange() {
        dirty = false;
        invalid = true;
    }


    const deleteConfirm = async () => {

    }
</script>

<Dialog
        bind:open={deleteVisible}
        aria-labelledby="simple-title"
        aria-describedby="simple-content"
>
    <Title id="simple-title">定义个人空间</Title>
    <Content id="simple-content">
        <Textfield
            type="text"
            bind:dirty
            bind:invalid
            bind:value
            label="空间id"
            style="min-width: 250px;"
            onchange={handlerChange}
        >
            {#snippet helper()}
                <HelperText validationMsg>That's not a valid email address.</HelperText>
            {/snippet}
        </Textfield>
    </Content>
    <Actions>
        <Button variant="outlined" color="secondary" onclick={() => ('No')}>
            <Label>取消</Label>
        </Button>
        <Button variant="raised" onclick={deleteConfirm}>
            <Label>确定</Label>
        </Button>
    </Actions>
</Dialog>

<style lang="scss">
  :global(.MuiListItem-root) {
    border-radius: 8px;
    margin-bottom: 8px;
    transition: background-color 0.2s;

    &:hover {
      background-color: rgba(0, 0, 0, 0.04);
    }
  }

  .document-tab{
    :global(.material-icons){
      color: #ff3e00;
      cursor: pointer;
      font-size: 12px;
    }
  }
</style>