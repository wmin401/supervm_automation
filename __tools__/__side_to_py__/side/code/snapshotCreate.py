
### Copy below function to your class ###


    def snapshotCreate(self):    
        printLog(printSquare('Snapshot Create'))
        result = FAIL
        msg = ''

        try:

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#compute > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#compute > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_vmsAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_vmsAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'MainVirtualMachineView_table_content_col2_row4')
            self.webDriver.findElement('id', 'MainVirtualMachineView_table_content_col2_row4', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '스냅샷')
            self.webDriver.findElement('link_text', '스냅샷', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_New')
            self.webDriver.findElement('id', 'DetailActionPanelView_New', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'VmSnapshotCreatePopupWidget_description')
            self.webDriver.findElement('id', 'VmSnapshotCreatePopupWidget_description', False)
            self.webDriver.sendKeys('') # You have to change this you want to write
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[SNAPSHOT CREATE] " + msg)

        # 결과 출력
        printLog("[SNAPSHOT CREATE] RESULT : " + result)
        self._snapshotResult.append(['snapshot' + DELIM + 'create' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('SNAPSHOT_CREATE',result, msg)