# terminal input handler
def terminal_input(promp_title = '> ', default_value = None):
    input_value = input(promp_title)
    input_value = input_value if input_value != '' else default_value
    return input_value

# grid configuration
class GridConfiguration:
    def __init__(self):
        self.grid_container_width = '100%'
        self.grid_columns = '12'
        self.grid_x_gap = '0px'
        self.grid_y_gap = '0px'
        self.grid_breakpoints = {
            'xm': '320px',
            'sm': '480px',
            'md': '768px',
            'lg': '1024px',
            'xl': '1200px'
        }

# grid builder
class GridBuilder:
    def __init__(self, grid_configuration: GridConfiguration = None):
        self.grid_configuration = grid_configuration
        self.grid_file = None

    def change_configuration(self, grid_configuration: GridConfiguration):
        self.grid_configuration = grid_configuration

    def grid_build(self):
        grid_file = """\r:root {
        \r  --grid-container-width: %s;
        \r  --grid-x-gap: %s;
        \r  --grid-y-gap: %s;
        \r}
        """ % (self.grid_configuration.grid_container_width,
               self.grid_configuration.grid_x_gap,
               self.grid_configuration.grid_y_gap)

        grid_file += """
        \r.grid-container {
        \r  width: var(--grid-container-width);
        \r}
        """
        
        grid_file += """
        \r.grid-x {
        \r  margin-left: calc(var(--grid-x-gap) / 2 * -1);
        \r  margin-right: calc(var(--grid-x-gap) / 2 * -1);

        \r  margin-top: calc(var(--grid-y-gap) / 2 * -1);
        \r  margin-bottom: calc(var(--grid-y-gap) / 2 * -1);

        \r  display: flex;
        \r  flex-wrap: wrap;
        \r}
        """

        grid_file += """
        \r.grid-y {
        \r  flex-basis: 100%;
        \r  padding-left: calc(var(--grid-x-gap) / 2);
        \r  padding-right: calc(var(--grid-x-gap) / 2);
    
        \r  padding-top: calc(var(--grid-y-gap) / 2);
        \r  padding-bottom: calc(var(--grid-y-gap) / 2);

        \r  box-sizing: border-box;
        \r  width: 100%;
        \r}"""

        breakpoints_keys = list(self.grid_configuration.grid_breakpoints.keys())
        
        for i in range(5):
            grid_file += '\n\n\r@media screen and (width > %s) {' % (
                self.grid_configuration.grid_breakpoints[breakpoints_keys[i]])

            for j in range(int(self.grid_configuration.grid_columns)):
                grid_file += '\n  .grid-y-%s-%s { flex-basis: %s; }' % (
                    breakpoints_keys[i], j + 1,
                    ('%s' % round(((j + 1) / int(self.grid_configuration.grid_columns)) * 100, 5)) + '%')

            grid_file += '\n}'
        return grid_file
               
if __name__ == '__main__':
    grid_configuration = GridConfiguration()
    grid_builder = GridBuilder(grid_configuration)

    print('\nCss Grid Builder ')
    
    grid_configuration.grid_container_width = terminal_input('~ Grid container width (default: 100%)> ', '100%')
    grid_configuration.grid_columns = terminal_input('~ Grid number of columns (default: 12)> ', '12')
    grid_configuration.grid_x_gap = terminal_input('~ Grid x gap (default: 0px)> ', '0px')
    grid_configuration.grid_y_gap = terminal_input('~ Grid y gap (default: 0px)> ', '0px')

    breakpoints_keys = list(grid_configuration.grid_breakpoints.keys())
    print('\nBreakpoints')
    breakpoints_question = terminal_input('~ Change default breakpoints (y)es or (n)o (default: n)> ', 'n')

    if breakpoints_question == 'y':
        for i in range(len(breakpoints_keys)):
            input_title = '~ Grid %s breakpoint: (default: %s)> ' % (
                breakpoints_keys[i],
                grid_configuration.grid_breakpoints[breakpoints_keys[i]])
            grid_configuration.grid_breakpoints[breakpoints_keys[i]] = terminal_input(
                input_title,
                grid_configuration.grid_breakpoints[breakpoints_keys[i]])

    print('\nFile')
    grid_builder.grid_file = terminal_input('~ File name (default: grid.css)> ', 'grid.css')
    
    file = open(grid_builder.grid_file, 'w')
    file.write(grid_builder.grid_build())
