
### Copy below function to your class ###


    def monitoringPortal(self):    
        printLog(printSquare('Monitoring Portal'))
        result = FAIL
        msg = ''

        try:

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#compute > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#compute > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_clustersAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_clustersAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'MainClusterView_table_content_col1_row0')
            self.webDriver.findElement('id', 'MainClusterView_table_content_col1_row0', True)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[MONITORING PORTAL] " + msg)

        # 결과 출력
        printLog("[MONITORING PORTAL] RESULT : " + result)
        self._monitoringResult.append(['monitoring' + DELIM + 'portal' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('MONITORING_PORTAL',result, msg)