'use client'

import { useState, useCallback } from 'react';
import {Classes, ContextMenu, Icon, Intent, Spinner, Tooltip, Tree, type TreeNodeInfo} from "@blueprintjs/core";
import { useFolders } from "../api/hooks";
import { each } from 'lodash';


type NodePath = number[];


export default function StorageTree() {

    const { folders, isError, isLoading } = useFolders();

    const handleNodeDblClick = useCallback(
        (node: TreeNodeInfo, nodePath: NodePath, e: React.MouseEvent<HTMLElement>) => {
            console.log("handleNodeClick");
        }, []
    );

    const contentSizing = { popoverProps: { popoverClassName: Classes.POPOVER_CONTENT_SIZING } };

    const getTreeNodeInfo = () => {

        const INITIAL_STATE: TreeNodeInfo[] = [
            {
                id: 0,
                hasCaret: true,
                icon: "folder-close",
                label: (
                    <ContextMenu {...contentSizing} content={<div>Hello there!</div>}>
                        Folder 0
                    </ContextMenu>
                ),
            },
            {
                id: 1,
                icon: "folder-close",
                isExpanded: true,
                label: (
                    <ContextMenu {...contentSizing} content={<div>Hello there!</div>}>
                        <Tooltip content="I'm a folder <3" placement="right">
                            Folder 1
                        </Tooltip>
                    </ContextMenu>
                ),
                childNodes: [
                    {
                        id: 2,
                        icon: "document",
                        label: "Item 0",
                        secondaryLabel: (
                            <Tooltip content="An eye!">
                                <Icon icon="eye-open" />
                            </Tooltip>
                        ),
                    },
                    {
                        id: 3,
                        icon: <Icon icon="tag" intent={Intent.PRIMARY} className={Classes.TREE_NODE_ICON} />,
                        label: "Organic meditation gluten-free, sriracha VHS drinking vinegar beard man.",
                    },
                    {
                        id: 4,
                        hasCaret: true,
                        icon: "folder-close",
                        label: (
                            <ContextMenu {...contentSizing} content={<div>Hello there!</div>}>
                                <Tooltip content="foo" placement="right">
                                    Folder 2
                                </Tooltip>
                            </ContextMenu>
                        ),
                        childNodes: [
                            { id: 5, label: "No-Icon Item" },
                            { id: 6, icon: "tag", label: "Item 1" },
                            {
                                id: 7,
                                hasCaret: true,
                                icon: "folder-close",
                                label: (
                                    <ContextMenu {...contentSizing} content={<div>Hello there!</div>}>
                                        Folder 3
                                    </ContextMenu>
                                ),
                                childNodes: [
                                    { id: 8, icon: "document", label: "Item 0" },
                                    { id: 9, icon: "tag", label: "Item 1" },
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                id: 2,
                hasCaret: true,
                icon: "folder-close",
                label: "Super secret files",
                disabled: true,
            },
        ];
        //return INITIAL_STATE;
        const state: TreeNodeInfo[] = [];
        each(folders, folder => {
            console.log(folder);
            state.push({
                id: 0,
                hasCaret: true,
                icon: "folder-open",
                label: (
                    <ContextMenu {...contentSizing} content={<div>Hello there!</div>}>
                        {folder.name}
                    </ContextMenu>
                )
            })
        });
        return state;
    }
    
    
    if(isLoading) {
        return <Spinner />;
    } else if(isError) {
        return <div>Error</div>;
    }
    return (
        <Tree
            contents={getTreeNodeInfo()}
            onNodeDoubleClick={handleNodeDblClick}
            className={Classes.ELEVATION_0}
        />
    )
}