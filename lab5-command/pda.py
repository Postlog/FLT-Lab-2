class Transit:
    def __init__(self, node_from, node_to, alphabeth_unit, stack_pop_symbol, stack_push_symbols, flags):
        self.node_from = node_from
        self.node_to = node_to
        self.type = alphabeth_unit[0]
        self.alphabeth_symbol = alphabeth_unit[1] if alphabeth_unit[0] == 'alphabeth_symbol' else alphabeth_unit[0]
        self.stack_pop_symbol = stack_pop_symbol[1] if len(stack_pop_symbol) == 2 else stack_pop_symbol[0]
        self.stack_push_symbols = list(map(lambda x: x[1] if len(x) == 2 else x[0], stack_push_symbols))
        self.flags = set(flags)


class PDA:
    def __init__(self, ast):
        self.raw_ast = ast
        self.nodes = set()
        self.inits = set()
        self.finals = set()
        self.traps = set()
        self.transits = set()
        self.labels = {}
        for block in ast:
            if block[0] == 'single_node_description':
                block = block[1]
                node_id = block['id']
                self.nodes.add(node_id)

                node_label = block['label']
                if node_label is not None:
                    self.labels[node_id] = node_label

                flags = set(block['flags'])
                if ('final_flag',) in flags:
                    self.finals.add(node_id)
                if ('initial_flag',) in flags:
                    self.inits.add(node_id)
                if ('trap_flag',) in flags:
                    self.traps.add(node_id)
                for transit in block['transits']:
                    transit_obj = Transit(
                        node_from=node_id,
                        node_to=transit['dest_id'],
                        alphabeth_unit=transit['alphabeth_unit'],
                        stack_pop_symbol=transit['stack_pop_symbol'],
                        stack_push_symbols=transit['stack_push_symbols'],
                        flags=transit['flags']
                    )
                    self.transits.add(transit_obj)
            elif block[0] == 'single_transit_description':
                block = block[1]
                transit_obj = Transit(
                    node_from=block['node_from'],
                    node_to=block['node_to'],
                    alphabeth_unit=block['alphabeth_unit'],
                    stack_pop_symbol=block['stack_pop_symbol'],
                    stack_push_symbols=block['stack_push_symbols'],
                    flags=block['flags']
                )
                self.transits.add(transit_obj)
            elif block[0] == 'group_of_nodes':
                block = block[1]
                flags = set(block['flags'])
                if ('final_flag',) in flags:
                    self.finals.update(block['nodes'])
                if ('initial_flag',) in flags:
                    self.inits.update(block['nodes'])
                if ('trap_flag',) in flags:
                    self.traps.update(block['nodes'])