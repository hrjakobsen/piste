from parser.core import AstVisitor, RestrictionProcessNode, InputProcessNode, TrueValueNode, FalseValueNode, \
    StringValueNode, IntegerValueNode, IdentifierNode, OutputProcessNode, ParallelProcessNode, InactionProcessNode, \
    ReplicatedInputProcessNode, ConditionalNode, ExternProcessNode, RecordNode, PathNode, BinaryExpressionNode


class BodyVisitor(AstVisitor):
    def visit_true_value_node(self, node: TrueValueNode):
        return "(piste_value){ .type = BOOL, .value = 1 }"

    def visit_false_value_node(self, node: FalseValueNode):
        return "(piste_value){ .type = BOOL, .value = 1 }"

    def visit_string_value_node(self, node: StringValueNode):
        return "(piste_value){ .type = STRING, .value = (long) \"" + node.value + "\" }"

    def visit_integer_value_node(self, node: IntegerValueNode):
        return "(piste_value){{ .type = INT, .value = {}}}".format(node.value)

    def visit_record_node(self, node: RecordNode):
        record_content = []
        for (name, val) in node.value:
            record_content.append(".{} = {}".format(name, val.accept(self)))
        return "((piste_value){{ .type = RECORD, .value = (long)&((struct {record_name}) {{ {record_content} }}) }})".format(
            record_name=node.type.value,
            record_content=", ".join(record_content)
        )

    def visit_path_node(self, node: PathNode):
        return "(((struct {type}*)({value}.value))->{field_name})".format(
            type=node.type.value,
            value=node.value.accept(self),
            field_name=node.field_name.value
        )

    def visit_identifier_node(self, node: IdentifierNode):
        return str(node.value)

    def visit_input_process_node(self, node: InputProcessNode):
        free_var_initialization = []
        for i, free_variable in enumerate(node.free_variables):
            free_var_initialization.append("        free_vars[{}] = {};".format(i, free_variable))
        return """
    {{
        piste_value* free_vars = (piste_value*)malloc(sizeof(piste_value) * {num_free_variables});
{free_var_initialization}
        closure_t* new_closure = alloc_closure({process_name}, {num_free_variables}, free_vars);
        queue_process(new_closure);
    }}""".format(
            num_free_variables=len(node.free_variables),
            process_name=node.name,
            free_var_initialization="\n".join(free_var_initialization)
        )

    def visit_replicated_input_process_node(self, node: ReplicatedInputProcessNode):

        free_var_initialization = []
        for i, free_variable in enumerate(node.free_variables):
            free_var_initialization.append("        free_vars[{}] = {};".format(i, free_variable))
        return """
    {{
        piste_value* free_vars = (piste_value*)malloc(sizeof(piste_value) * {num_free_variables});
{free_var_initialization}
        closure_t* new_closure = alloc_closure({process_name}, {num_free_variables}, free_vars);
        add_replicated_reader(new_closure, {channel});
    }}
        """.format(
            num_free_variables=len(node.free_variables),
            process_name=node.name,
            free_var_initialization="\n".join(free_var_initialization),
            channel=node.receiver.accept(self)
        )

    def visit_output_process_node(self, node: OutputProcessNode):
        receiver = node.receiver.accept(self)
        declarations = []
        for value in node.values:
            declarations.append("    insert_message({}, {});".format(
                receiver,
                value.accept(self)
            ))
        return "\n".join(declarations)

    def visit_parallel_process_node(self, node: ParallelProcessNode):
        return "{}\n{}".format(node.left.accept(self), node.right.accept(self))

    def visit_restriction_process_node(self, node: RestrictionProcessNode):
        return "    piste_value {} = alloc_channel();\n{}".format(node.identifier.value, node.continuation.accept(self))

    def visit_inaction_process_node(self, node: InactionProcessNode):
        return "/* inaction */"

    def visit_conditional_node(self, node: ConditionalNode):
        return """
    if ({predicate}.value) {{
        {true_branch}
    }} else {{
        {false_branch}
    }}
        """.format(predicate=node.predicate.accept(self),
                   true_branch=node.true_branch.accept(self),
                   false_branch=node.false_branch.accept(self))

    def visit_extern_process_node(self, node: ExternProcessNode):
        free_var_initialization = []
        return """
    piste_value {channel} = alloc_channel();
    {{
        piste_value* free_vars = (piste_value*)malloc(sizeof(piste_value));
        free_vars[0] = {channel};
        closure_t* new_closure = alloc_closure({process_name}, 1, free_vars);
        add_replicated_reader(new_closure, {channel});
    }}
                \n""".format(
            num_free_variables=0,
            process_name=node.name,
            free_var_initialization="\n".join(free_var_initialization),
            channel=node.internal_name.accept(self)
        ) + node.continuation.accept(self)

    def visit_binary_expression_node(self, node: BinaryExpressionNode):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if node.operation == BinaryExpressionNode.POWER:
            return "((piste_value){{ .type = INT, .value = (pow(({}).value, ({}).value))}})".format(left, right)
        else:
            return "((piste_value){{ .type = INT, .value = (({}).value {} ({}).value)}})".format(
                left,
                node.operation,
                right
            )


class DeclarationVisitor(AstVisitor):
    def __init__(self):
        self.declarations = []
        self.prototypes = []
        self.records = {}
        self.body_visitor = BodyVisitor()

    def visit_input_process_node(self, node: InputProcessNode):
        free_variables = node.free_variables
        free_variables = sorted(free_variables)
        free_var_decls = []
        free_var_initialization = []
        for i, fv in enumerate(free_variables):
            free_var_decls.append(
                "    piste_value {} = closure->free_variables[{}];".format(fv, i)
            )
            free_var_initialization.append("        free_vars[{}] = {};".format(i, fv))

        free_variables_str = "\n".join(free_var_decls) + "\n"
        received_messages = []
        for name in node.identifiers:
            received_messages.append("        piste_value {} = read_message({});".format(name.value, node.receiver.value))
        self.prototypes.append("int {}(closure_t* closure);".format(node.name))
        self.declarations.append({
            "name": node.name,
            "body": """
int {name}(closure_t* closure) {{
    // Initialize free variables
{free_variables}
    // Receive message
    if (has_message({channel})) {{
{received_messages}
    {process}
    return 1;
    }} else {{
        return 0;
    }}
}}
        """.format(name=node.name,
                   free_variables=free_variables_str,
                   channel=node.receiver.value,
                   process=node.continuation.accept(self.body_visitor),
                   num_free_variables=len(node.free_variables),
                   process_name=node.name,
                   received_messages="\n".join(received_messages),
                   free_var_initialization="\n".join(free_var_initialization))})
        for identifier in node.identifiers:
            identifier.accept(self)
        node.continuation.accept(self)

    def visit_replicated_input_process_node(self, node: ReplicatedInputProcessNode):
        free_variables = node.free_variables
        free_variables = sorted(free_variables)
        free_var_decls = []
        free_var_initialization = []
        for i, fv in enumerate(free_variables):
            free_var_decls.append(
                "    piste_value {} = closure->free_variables[{}];".format(fv, i)
            )
            free_var_initialization.append("        free_vars[{}] = {};".format(i, fv))

        free_variables_str = "\n".join(free_var_decls) + "\n"
        received_messages = []
        for name in node.identifiers:
            received_messages.append("        piste_value {} = read_message({});".format(name.value, node.receiver.value))

        self.prototypes.append("int {}(closure_t* closure);".format(node.name))
        self.declarations.append({
            "name": node.name,
            "body": """
int {name}(closure_t* closure) {{
    // Initialize free variables
{free_variables}
    // Receive message
    if (has_message({channel})) {{
{received_messages}
        {process}
        return 1;
    }} else {{
        return 0;
    }}
}}
        """.format(name=node.name,
                   free_variables=free_variables_str,
                   received_messages="\n".join(received_messages),
                   channel=node.receiver.value,
                   process=node.continuation.accept(self.body_visitor),
                   num_free_variables=len(node.free_variables),
                   process_name=node.name,
                   free_var_initialization="\n".join(free_var_initialization))})
        for identifier in node.identifiers:
            identifier.accept(self)
        node.continuation.accept(self)

    def visit_extern_process_node(self, node: ExternProcessNode):
        node.external_name.accept(self)
        node.internal_name.accept(self)
        self.prototypes.append("extern piste_value {}({});".format(node.external_name.value, ", ".join(["piste_value"] * len(node.arg_types))))
        self.prototypes.append("int {}(closure_t* closure);".format(node.name))

        arg_list = []
        args = []
        for i in range(len(node.arg_types)):
            arg_name = "arg_" + str(i)
            arg_list.append(arg_name)
            args.append("    piste_value {} = read_message({});".format(arg_name, node.internal_name.value))

        self.declarations.append({"name": node.name, "body": """
int {process_name}(closure_t* closure) {{
    // {piste_name}
    piste_value {channel_name} = closure->free_variables[0];
{arguments}
    piste_value result_channel = read_message({channel_name});
    piste_value result = {external_name}({arg_list});
    insert_message(result_channel, result);
    return 1;
}}
        """.format(
            process_name=node.name,
            piste_name=node.internal_name.value,
            arguments="\n".join(args),
            channel_name=node.internal_name.value,
            external_name=node.external_name.value,
            arg_list=", ".join(arg_list)
        )})

        node.continuation.accept(self)

    def visit_record_node(self, node: RecordNode):
        if node.type.value not in self.records:
            entries = []
            for (name, _) in node.value:
                entries.append("piste_value " + name + ";")
            self.records[node.type.value] = "struct {} {{ {} }};".format(node.type.value, " ".join(entries))
        super().visit_record_node(node)


def entry_point(body):
    return """
int piste_entry(closure_t* closure) {{
    {};
    return 1;
}}
""".format(body)


def front_matter():
    return """
#include "piste.h"
#include <malloc.h>
#include <math.h>
"""


def generate_c_code(ast):
    declaration_visitor = DeclarationVisitor()
    body_visitor = BodyVisitor()
    ast.accept(declaration_visitor)

    res = ""

    res += front_matter()

    for prototype in declaration_visitor.prototypes:
        res += "\n" + prototype

    for record in declaration_visitor.records:
        res += "\n" + declaration_visitor.records[record]

    for declaration in declaration_visitor.declarations:
        res += "\n" + declaration["body"]

    res += "\n" + entry_point(ast.accept(body_visitor))
    return res
